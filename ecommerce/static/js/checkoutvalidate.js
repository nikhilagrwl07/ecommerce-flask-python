function validate() {
debugger
    var addr = document.getElementById("adr").value;
    if(",#-/ !@$%^*(){}|[]\\$".indexOf(addr) >= 0)
        phone=document.getElementById("phone").value;
        if(phone.includes("+1"))
            if(phone.length==12)
                zip=document.getElementById("zip").value;
                if(zip.length==5 && zip.match("^[0-9]"))))
                    return true
                 else
                    alert("enter valid zi,it should be numberic and no more than 5 digits")
            else
                alert("number not valid")
                    return false
        else
            alert("Please add +1 for country code");
            return false;
        return true
    else
        alert("Address not valid");
        return false;

}