var markupInput, canvas, context, strawHat = new Image(41,37),
	skullW = 25, skullH = 12, bezNudge = 2, skullMid = skullW/2,
	eyeR = 3.6, dotR = 1.6,
	jawI = 5, jawSmI = 6, jawDmin = 16, jawDmax = 18, jawUmin = 6.5, jawUmax = 8.5,
	teethGap = 5, teethHS = 3, teethHL = 5, teethLineWeight = 2.5,
	scalpI = 1, scalpMin = 5.5, scalpMax = 10,
	hornHS = 4, hornHL = 9, hornCL = 2, hornCS = 0.75, hornLineWeight = 2.2,
	spaceXS = 30, spaceXL = 40, spaceY = 50, marginX = 16, marginY = 25,
	parenRegEx = /[\(\)]/;
strawHat.src = "pics/strawHatSkull.png";

window.addEventListener("load",function(){
	markupInput = document.getElementById("markupInput");
	canvas = document.getElementById("skullCanvas");
	context = canvas.getContext("2d");
	
	context.lineCap = "round";
	context.fillStyle = "#FFF";
	context.strokeStyle = "#FFF";
	
	updateSkullDisplay();
	markupInput.addEventListener("change",updateSkullDisplay);
	markupInput.addEventListener("keyup",updateSkullDisplay);
});

function updateSkullDisplay(){
	drawSkullArray(context, canvas, getSkullArray(markupInput.value));
}

function drawSkullArray(ctx, canvas, skulls){
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	var i, x = marginX, y = marginY;
	for(i=1;i<skulls.length;i+=2){ // By twos
		drawSkull(ctx, x, y, skulls[i-1]);
		x += spaceXS;
		drawSkull(ctx, x, y, skulls[i]);
		x += spaceXL;
		if(x+spaceXS+skullW+marginX >= canvas.width){
			x = marginX;
			y += spaceY;
		}
	}
	if(i-1 < skulls.length){
		drawSkull(ctx, x, y, skulls[i-1]);
	}
}

function drawSkull(ctx, x, y, skull){
	if(skull.piece == 1){
		ctx.drawImage(strawHat,x-8,y-17);
		return;
	}
	var marks = skull.markup.split(parenRegEx);
	// Draw main skull
	ctx.beginPath();
	ctx.moveTo(x,y);
	ctx.bezierCurveTo(x-bezNudge,y+skullH,x+skullW+bezNudge,y+skullH,x+skullW,y);
	ctx.bezierCurveTo(x+skullW+bezNudge,y-skullH,x-bezNudge,y-skullH,x,y);
	// Draw eyes
	var eyeSpread = (skullW+bezNudge+bezNudge) / (marks[1].length+1);
	var eyeX = x + eyeSpread - bezNudge;
	for(var i=0;i<marks[1].length;++i){
		circle(ctx,eyeX,y,eyeR);
		if(marks[1].charAt(i)==".") circle(ctx,eyeX,y,dotR);
		eyeX += eyeSpread;
	}
	ctx.fill();
	// Draw teeth
	var teeth = parseInt(marks[2],10), topTeeth, botTeeth;
	ctx.lineWidth = teethLineWeight;
	ctx.beginPath();
	if(teeth>4){
		topTeeth = botTeeth = Math.floor(teeth/2);
		if(teeth%2==1) ++botTeeth;
		if(botTeeth==3){
			ctx.moveTo(x+jawSmI,y+jawDmin);
			ctx.bezierCurveTo(
				x+jawSmI,y+jawDmax,
				x+skullW-jawSmI,y+jawDmax,
				x+skullW-jawSmI,y+jawDmin);
		}else{
			ctx.moveTo(x+jawI,y+jawDmin);
			ctx.bezierCurveTo(
				x+jawI,y+jawDmax,
				x+skullW-jawI,y+jawDmax,
				x+skullW-jawI,y+jawDmin);
		}
		drawSpikes(ctx,
			x+jawI,y+jawDmin,
			x+jawI,y+jawDmax,
			x+skullW-jawI,y+jawDmax,
			x+skullW-jawI,y+jawDmin,
			filledArray(-teethHS, botTeeth));
	}else{
		topTeeth = teeth;
		botTeeth = 0;
	}
	drawSpikes(ctx,
		x+jawI,y+jawUmin,
		x+jawI,y+jawUmax,
		x+skullW-jawI,y+jawUmax,
		x+skullW-jawI,y+jawUmin,
		filledArray(botTeeth>0 ? teethHS:teethHL, topTeeth));
	ctx.stroke();
	// Draw horns
	ctx.lineWidth = hornLineWeight;
	ctx.beginPath();
	var horns = [], curves = [];
	for(var i=0;i<marks[0].length;++i){
		if(marks[0].charAt(i)=="!"){
			horns[i] = -hornHL;
			curves[i] = hornCL;
		}else{
			horns[i] = -hornHS;
			curves[i] = hornCS;
		}
	}
	drawSpikes(ctx,
		x+scalpI,y-scalpMin,
		x+scalpI,y-scalpMax,
		x+skullW-scalpI,y-scalpMax,
		x+skullW-scalpI,y-scalpMin,
		horns, curves);
	ctx.stroke();
	return true;
}

function circle(ctx, x, y, r){
	ctx.moveTo(x+r,y);
	ctx.arc(x,y,r,0,2*Math.PI);
}

var spikePosCache = [
	[],										//0
	[0.5],									//1
	[0.37,0.63],							//2
	[0.2,0.5,0.8],							//3
	[0,0.37,0.63,1],						//4
	[0,0.32,0.5,0.68,1],					//5
	[0,0.28,0.43,0.57,0.72,1],				//6
	[0,0.25,0.38,0.5,0.62,0.75,1],			//7
	[0,0.23,0.35,0.45,0.55,0.65,0.77,1],	//8
	[0,0.21,0.33,0.43,0.5,0.57,0.67,0.79,1]	//9
];
function drawSpikes(ctx,p0x,p0y,c0x,c0y,c1x,c1y,p1x,p1y,lengths,curves){
	var ptOn, t, curveMul;
	if(lengths.length < spikePosCache.length){
		t = spikePosCache[lengths.length];
	}else{
		t = [];
		for(var i=0;i<lengths.length;++i){
			t[i] = i / (lengths.length-1);
		}
	}
	for(var i = 0; i < t.length; ++i){
		ptOn = pointOnBezier(p0x,p0y,c0x,c0y,c1x,c1y,p1x,p1y,t[i]);
		ctx.moveTo(ptOn.x,ptOn.y);
		if(curves){
			//if(t[i]>0.9) curveMul = 0.7;
			if(t[i]>0.5) curveMul = 1;
			//else if(t[i]<0.1) curveMul = -0.7;
			else if(t[i]<0.5) curveMul = -1;
			else curveMul = 0;
			ctx.bezierCurveTo(
				ptOn.x+curves[i]*curveMul,ptOn.y+lengths[i]/3,
				ptOn.x+curves[i]*curveMul,ptOn.y+(lengths[i]+lengths[i])/3,
				ptOn.x,ptOn.y+lengths[i]);
		}else{
			ctx.lineTo(ptOn.x,ptOn.y+lengths[i]);
		}
	}
}

function pointOnBezier(p0x,p0y,c0x,c0y,c1x,c1y,p1x,p1y,t){
	if(t<=0) return {x: p0x, y: p0y};
	if(t>=1) return {x: p1x, y: p1y};
	//step 1
	var Ax = ( (1 - t) * p0x ) + (t * c0x),
		Ay = ( (1 - t) * p0y ) + (t * c0y),
		Bx = ( (1 - t) * c0x ) + (t * c1x),
		By = ( (1 - t) * c0y ) + (t * c1y),
		Cx = ( (1 - t) * c1x ) + (t * p1x),
		Cy = ( (1 - t) * c1y ) + (t * p1y),
	//step 2
		Dx = ( (1 - t) * Ax ) + (t * Bx),
		Dy = ( (1 - t) * Ay ) + (t * By),
		Ex = ( (1 - t) * Bx ) + (t * Cx),
		Ey = ( (1 - t) * By ) + (t * Cy);
	//step 3
	return {
		x: ( (1 - t) * Dx ) + (t * Ex),
		y: ( (1 - t) * Dy ) + (t * Ey)
	};
}

function filledArray(v,l){
	var arr = [];
	for(var i=0;i<l;++i){
		arr[i] = v;
	}
	return arr;
}