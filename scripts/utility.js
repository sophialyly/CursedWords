var textContentRegEx = /\t|^[\r\n|\n|\r]|[\r\n|\n|\r]$/g;

window.addEventListener("load",function(){
	var exps = document.getElementsByClassName("expandable");
	for(var i=0;i<exps.length;++i){
		exps[i].firstElementChild.addEventListener("click",toggleExpand);
	}
	var butts = document.getElementsByClassName("copyMarkupButton");
	for(var lol=0;lol<butts.length;++lol){
		butts[lol].addEventListener("click",copyMarkup);
	}
});

function toggleExpand(){
	var tabIndex, expandable = this.parentElement;
	if(expandable.classList.contains("minimized")){
		expandable.classList.remove("minimized");
		tabIndex = 0;
	}else{
		expandable.classList.add("minimized");
		tabIndex = -1;
	}
	var tabbable = expandable.querySelectorAll(".expandableContent a, .expandableContent button");
	for(var i=0;i<tabbable.length;++i){
		tabbable[i].tabIndex = tabIndex;
	}
}

function copyMarkup(){
	var tds = this.parentElement.parentElement.children;
	var innerText = tds[tds[2].textContent.length > 0 ? 2 : 1]
		.textContent.replace(textContentRegEx,"");
	console.log(innerText);
	markupInput.value = innerText;
	updateSkullDisplay();
	history.pushState({}, "", this.href);
	window.scrollTo(0,0);
}