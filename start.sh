# Open port 22442 for all VM instances to external!

export PROJECT_ID=`gcloud config get-value project`
export ZONE=us-central1-a
export CLUSTER_NAME=${PROJECT_ID}-1
export MACHINE_TYPE=n1-standard-1

services=(host-proxy host-a host-bc)
LOADS=(const_10 const_20 const_30 const_40 const_50 const_60 const_70 training)

# setup nodes
gcloud container clusters create $CLUSTER_NAME --min-nodes=${#services[@]} --max-nodes=${#services[@]} --num-nodes=${#services[@]} --zone $ZONE --machine-type=${MACHINE_TYPE} --no-enable-autoupgrade
nodes_string=`kubectl get nodes | grep -vP '^NAME' | grep -oP '^[\w\-0-9]+'`
readarray -t nodes <<< "$nodes_string"
IP_LIST=()
for index in "${!services[@]}"
do
	kubectl label nodes ${nodes[index]} service=${services[index]}	# label the nodes to specific services
	gcloud compute scp lmdaemon ${nodes[index]}:~ --zone=$ZONE --quiet	# copy and start our utilization measurement tool, port: 22442
	gcloud compute ssh ${nodes[index]} --zone=$ZONE --quiet --command="chmod +x lmdaemon; sudo mount -o remount,rw,exec /home; nohup ~/lmdaemon > /dev/null 2>&1 &"
	NODE_IP="$(gcloud compute instances describe ${nodes[index]} --zone=${ZONE} --format='get(networkInterfaces[0].accessConfigs[0].natIP)')"
	IP_LIST+=($NODE_IP)
done
kubectl apply -f ./kubernetes-manifests	# deploys specially prepared delays
echo "waiting for system to boot up... (3 minutes)"
sleep 180
kubectl get pods -o wide	# show deployment of pods for verification

# prepare settings for loadgenerator
PROXY_ADDR="http://${IP_LIST[0]}:8080/SyntheticComponents/"
A_ADDR="http://${IP_LIST[1]}:8080/SyntheticComponents/"
BC_ADDR="http://${IP_LIST[2]}:8080/SyntheticComponents/"
cp load.lua load_backup.lua
sed -i "s@PROXYURLPLACEHOLDER@${PROXY_ADDR}indexA@g" load.lua
LMDAEMON_PORT="22442"
IP_STRING=""
for ip in "${IP_LIST[@]}"; do IP_STRING+="${ip}:${LMDAEMON_PORT}," ; done
echo "PROXY_ADDR: ${PROXY_ADDR}"
echo "A_ADDR: ${A_ADDR}"
echo "BC_ADDR: ${BC_ADDR}"
echo "IP STRING: ${IP_STRING}"

# execute measurements for all loads
for LOAD in ${LOADS}
do
	echo "starting loadgenerator for load ${LOAD}."
	java -jar httploadgenerator.jar loadgenerator & java -cp load.jar:httploadgenerator.jar tools.descartes.dlim.httploadgenerator.runner.Main director --ip localhost --load loads/${LOAD}.csv -o scenario_logs/${LOAD}.csv --lua load.lua -t 256 -p="${IP_STRING::${#IP_STRING}-1}" -c measurment.ProcListener
	pkill -f 'java -jar'
	# saving logs
	mkdir logs/${LOAD}
	curl ${A_ADDR}extB -o logs/${LOAD}/B.csv
	curl ${A_ADDR}extC -o logs/${LOAD}/C.csv
	curl ${PROXY_ADDR}extA -o logs/${LOAD}/A.csv
	# reset components
	curl ${PROXY_ADDR}reset
	curl ${A_ADDR}reset
	curl ${BC_ADDR}reset
	echo "finished experiment ${LOAD}."
done

cp load_backup.lua load.lua
rm -f load_backup.lua
gcloud container clusters delete $CLUSTER_NAME --zone=$ZONE --quiet
