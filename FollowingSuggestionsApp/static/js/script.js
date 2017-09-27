window.onload=function(){
	var btnSubmit = document.getElementById("submit");
	btnSubmit.addEventListener("click", getSuggestion);	
};

function getSuggestion(){
	var username = document.getElementById("username").value;
	var progress = document.getElementById("progress");
	progress.style.visibility="visible";
	
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", "getFollowingSuggestion?username=" + username, true);
	xhttp.onreadystatechange= function(){
		if(this.readyState==4 && this.status ==200){
			progress.style.visibility="hidden";
			resp = JSON.parse(this.responseText);
			//alert("response returned!");
			var searchDiv = document.getElementById("search");
			var div = document.createElement("div");
			div.className="card";
			
			if(resp.error!=null){
				var p = document.createElement("p");
				p.style.marginTop="20px";
				p.innerHTML="Sorry, " + username + " does not exist or doesn't follow any accounts";
				div.appendChild(p);
				searchDiv.appendChild(div);
			}else{
				var summary = document.createElement("div");
				summary.innerHTML="After analyzing <b>" + 
						resp.numAnalyzed + "</b> accounts, <b>" + resp.enteredUsername 
						+ "</b> should check out these accounts:";
				summary.style.marinBottom="4px";
				div.appendChild(summary);
				
				var resultList = document.createElement("ol");
				var suggestions = resp.suggestions;
				//alert(Array.isArray(suggestions));
				for(var i=0; i< suggestions.length; i++){
					var li = document.createElement("li");
					suggestion = suggestions[i];
					li.innerHTML="<a href='https://www.instagram.com/" + suggestion[0] 
						+ "' target='_blank'>" + suggestion[0] + "</a> had <b>" + suggestion[1] + "</b> common followings";
					resultList.appendChild(li);
				}
				resultList.style.width="80%";
				resultList.style.margin="auto";
				resultList.style.marginTop="8px";
				resultList.style.textAlign="left";
				div.appendChild(resultList);
				searchDiv.appendChild(div);
			}		
		}
	}
	//xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	//xhttp.send("username=" + username); <-- used for POST not GET
	xhttp.send();
}