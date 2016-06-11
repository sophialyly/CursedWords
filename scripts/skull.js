function Skull(horns,eyes,teeth,markup){
	if(typeof horns == "number"){
		this.horns = horns;
	}else if(horns == "👒"){
		this.piece = 1;
		this.markup = markup;
		return;
	}else{
		this.horns = parseHorns(horns);
	}
	if(typeof eyes == "number"){
		this.eyes = eyes;
	}else if (eyes === "X" || eyes === "x"){
		this.missing = true;
		this.markup = markup;
		return;
	}else{
		this.eyes = 0;
		for(var i=0;i<eyes.length;++i){
			if(eyes.charAt(i)===".") this.eyes++;
		}
	}
	this.teeth = teeth|0;

	if(markup===undefined){
		markup = unparseHorns(this.horns)+"(";
		if(this.eyes===0) markup += "oo";
		else if(this.eyes===2) markup += "..";
		else if(this.eyes===1){
			if(Math.random()>0.5) markup += "o.";
			else markup += ".o";
		}else for(var i=0;i<this.eyes;i++) markup += ".";
		markup += ")"+((this.teeth==0)?"":this.teeth);
	}
	this.markup = markup;
}
function parseHorns(str){
	var foundLong = false,
		tally = 0;
	for(var i=0;i<str.length;++i){
		if(str.charAt(i)==="!"){
			if(!foundLong){
				foundLong = true;
				tally = -tally;
			}
			tally += 5;
		}else if(str.charAt(i)===".") tally++;
	}
	return tally;
}
function unparseHorns(num){
	var str = "";
	if(num===4) str = ".!";
	else while(num>0){
		if(num>=5){
			str += "!";
			num -= 5;
		}else{
			str += ".";
			num--;
		}
	}
	return str;
}