function onCycle()
end

function onCall(callnum)
    if callnum == 1 then
        return "PROXYURLPLACEHOLDER"
    else
        return nil;
    end
end
