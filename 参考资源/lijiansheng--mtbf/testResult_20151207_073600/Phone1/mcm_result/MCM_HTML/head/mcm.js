var fs= require('fs');
var tmp=JSON.parse(fs.readFileSync("json/avg.json"));
var sleep = tmp.sleep;
var map_times = tmp.map_times;

function getact(t){
var path="json/hour_" + t + "/activity.json";
var data=JSON.parse(fs.readFileSync(path));
return data.act;}

function getdata(t){
var path="json/hour_" + t + "/data.json";
var data=JSON.parse(fs.readFileSync(path));
return data.data_time;}

function getcpu(a,t){
var path="json/hour_" + t + "/cpu.json";
var data=JSON.parse(fs.readFileSync(path));
var x;
switch (a){
	case 'loop':
		x=data.loop;
		break;
	case 'time':
		x=data.time;
		break;
}
var usr=[],sys=[],nic=[],idle=[],io=[],irq=[],sirq=[];
for (var i=0; i < x.length; i++) {
	usr.push({x:x[i],y:data.usr[i]});
	sys.push({x:x[i],y:data.sys[i]});
	nic.push({x:x[i],y:data.nic[i]});
	idle.push({x:x[i],y:data.idle[i]});
	io.push({x:x[i],y:data.io[i]});
	irq.push({x:x[i],y:data.irq[i]});
	sirq.push({x:x[i],y:data.sirq[i]})
}
var series=[];
series.push({name:'usr',data:usr});
series.push({name:'sys',data:sys});
series.push({name:'nic',data:nic});
series.push({name:'idle',data:idle});
series.push({name:'io',data:io});
series.push({name:'irq',data:irq});
series.push({name:'sirq',data:sirq})
return [x,series];}

function getcpuinfo(a,b,t){
	var cpuline_path="json/hour_" + t + "/cpuline.json";
	var cpuline=JSON.parse(fs.readFileSync(cpuline_path));
	var lta=[],x=[],cpu=[],tmp=[],series=[],path,data,pid=0;
	for (var i = 0; i < b.length; i++) {
		for (var j = 0; j < cpuline.maxcpu.length; j++) {
			if(cpuline.maxcpu[j][0] == b[i]){
				path="json/hour_" + t + "/" + cpuline.maxcpu[j][2] + ".json";
				data=JSON.parse(fs.readFileSync(path));
				lta.push([data.loop,data.time,data.avg]);
				switch (a){
					case 'loop':
						x=data.loop;
						break;
					case 'time':
						x=data.time;
						break;
				}
				for (var k=0; k < x.length; k++) {
					if(isArray(data.cpu[k]) == false){cpu.push({x:x[k],y:data.cpu[k]})}else{
						if(data.cpu[k].length == 2){cpu.push({x:x[k],y:data.cpu[k][0],marker:{enabled:true,fillColor:'#FF0000'}})}
						if(data.cpu[k].length == 3){
							if(pid==0){
								pid=data.cpu[k][3]
							}else{
								if(data.cpu[k][3] != pid){
									tmp.push({x:x[k],y:data.cpu[k][0],marker:{enabled:true,fillColor:'#FF0000'}})
								}else{
									tmp.push({x:x[k],y:data.cpu[k][0],marker:{enabled:true,fillColor:'#FFFF00'}})
								}
							}
						}
					}
				}
				if(tmp != []){
					cpu.push(null);
					cpu.push(tmp)
				}
				series.push({name:data.name,data:cpu});
				cpu=[];tmp=[];
				pid=0;
				break
			}
		}
	}
return [lta,series];}

function getcpuline(a,t){
	var path="json/hour_" + t + "/cpuline.json";
	var data=JSON.parse(fs.readFileSync(path));
	var l;
	if(a==-1){return data.maxcpu;}else{
	if(a==0||data.maxcpu.length<a){l=data.maxcpu.length}else{l=a}
	var rcpu=[]
	for (var i = 0; i < l; i++) {rcpu.push(data.maxcpu[i][0])}
return rcpu;}}

function getmem(a,b,t){
	var path="json/hour_" + t + "/mem.json";
	var data=JSON.parse(fs.readFileSync(path));
	var x;
	switch (a){
		case 'loop':
			x=data.loop
		break;
		case 'time':
			x=data.time
		break;
	}
	var series=[];
	switch (b){
	case 'free':
		var free=[],memfree=[],buffers=[],cached=[];
		var check=data.CMAFree[0];
		if(check!="NA"){var CMA=[]}
		for (var i=0; i < x.length; i++) {
			free.push({x:x[i],y:data.free[i]});
			memfree.push({x:x[i],y:data.memfree[i]});
			buffers.push({x:x[i],y:data.buffers[i]});
			cached.push({x:x[i],y:data.cached[i]});
			if(check!="NA"){CMA.push({x:x[i],y:data.CMAFree[i]})}
		}
		series.push({name:'Available_Memory',data:free});
		series.push({name:'MemFree',data:memfree});
		series.push({name:'Buffers',data:buffers});
		series.push({name:'Cached',data:cached});
		if(check!="NA"){series.push({name:'CMA_Free',data:CMA})}
		break;
	case 'all':
		var free=[],active=[],inactive=[],io=[],mapped=[],slab=[];
		for (var i=0; i < x.length; i++) {
			free.push({x:x[i],y:data.free[i]});
			active.push({x:x[i],y:data.active[i]});
			inactive.push({x:x[i],y:data.inactive[i]});
			io.push({x:x[i],y:data.io[i]});
			mapped.push({x:x[i],y:data.mapped[i]});
			slab.push({x:x[i],y:data.slab[i]})
		}
		series.push({name:'Available_Memory',data:free});
		series.push({name:'Active',data:active});
		series.push({name:'Inactive',data:inactive});
		series.push({name:'io',data:io});
		series.push({name:'Mapped',data:mapped});
		series.push({name:'Slab',data:slab});
		break;
	case 'io':
		var io=[],dirty=[],writeback=[];
		for (var i=0; i < x.length; i++) {
			io.push({x:x[i],y:data.io[i]});
			dirty.push({x:x[i],y:data.dirty[i]});
			writeback.push({x:x[i],y:data.writeback[i]});
		}
		series.push({name:'IO',data:io});
		series.push({name:'Dirty',data:dirty});
		series.push({name:'Writeback',data:writeback});
		break;
	case 'AI':
	var active=[],inactive=[],active_a=[],inactive_a=[],active_f=[],inactive_f=[];
		for (var i=0; i < x.length; i++) {
			active.push({x:x[i],y:data.active[i]});
			inactive.push({x:x[i],y:data.inactive[i]});
			active_a.push({x:x[i],y:data.active_a[i]});
			inactive_a.push({x:x[i],y:data.inactive_a[i]});
			active_f.push({x:x[i],y:data.active_f[i]});
			inactive_f.push({x:x[i],y:data.inactive_f[i]});
		}
		series.push({name:'Active',data:active});
		series.push({name:'Inactive',data:inactive});
		series.push({name:'Active(anon)',data:active_a});
		series.push({name:'Inactive(anon)',data:inactive_a});
		series.push({name:'Active(file)',data:active_f});
		series.push({name:'Inactive(file)',data:inactive_f});
		break;
	case 'MS':
	var mapped=[],slab=[];
	for (var i=0; i < x.length; i++) {
			mapped.push({x:x[i],y:data.mapped[i]});
			slab.push({x:x[i],y:data.slab[i]});
		}
		series.push({name:'Mapped',data:mapped});
		series.push({name:'Slab',data:slab});
		break;}
return [x,series];}

function getmeminfo(a,b,c,t){
	var pssline_path="json/hour_" + t + "/pssline.json";
	var pssline=JSON.parse(fs.readFileSync(pssline_path));
	var lta=[],series=[],path,data,x,pss=[],pid=0,tmp=[];
	var NHS=[],NHA=[],NHF=[],DHP=[],DHS=[],DHA=[],DHF=[],tmp1=[],tmp2=[],tmp3=[],tmp4=[],tmp5=[],tmp6=[],tmp7=[];
	for (var i = 0; i < b.length; i++) {
		for (var j = 0; j < pssline.maxpss.length; j++) {
			if(pssline.maxpss[j][0] == b[i]){
				path="json/hour_" + t + "/" + pssline.maxpss[j][2] + ".json";
				data=JSON.parse(fs.readFileSync(path));
				lta.push([data.loop,data.time,data.avg]);
				switch (a){
					case 'loop':
						x=data.loop;
						break;
					case 'time':
						x=data.time;
						break;
				}
				for (var k=0; k < x.length; k++) {
					if(isArray(data.pss[k]) == false){
						pss.push({x:x[k],y:data.pss[k]});
						if(data.type==1&&c==1){
							NHS.push({x:x[k],y:data.NHS[k]});
							NHA.push({x:x[k],y:data.NHA[k]});
							NHF.push({x:x[k],y:data.NHF[k]});
							DHP.push({x:x[k],y:data.DHP[k]});
							DHS.push({x:x[k],y:data.DHS[k]});
							DHA.push({x:x[k],y:data.DHA[k]});
							DHF.push({x:x[k],y:data.DHF[k]})
						}
					}else{
						if(data.pss[k].length == 2){
							pss.push({x:x[k],y:data.pss[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
							if(data.type==1&&c==1){
								NHS.push({x:x[k],y:data.NHS[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								NHA.push({x:x[k],y:data.NHA[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								NHF.push({x:x[k],y:data.NHF[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								DHP.push({x:x[k],y:data.DHP[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								DHS.push({x:x[k],y:data.DHS[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								DHA.push({x:x[k],y:data.DHA[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
								DHF.push({x:x[k],y:data.DHF[k][0],marker:{enabled:true,fillColor:'#FF0000'}})
							}
						}else{
							if(data.pss[k].length == 3){
								if(pid==0){
									pid=data.pss[k][3]
								}else{
									if(data.pss[k][3] != pid){
										tmp.push({x:x[k],y:data.pss[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
										if(data.type==1&&c==1){
											tmp1.push({x:x[k],y:data.NHS[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp2.push({x:x[k],y:data.NHA[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp3.push({x:x[k],y:data.NHF[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp4.push({x:x[k],y:data.DHP[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp5.push({x:x[k],y:data.DHS[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp6.push({x:x[k],y:data.DHA[k][0],marker:{enabled:true,fillColor:'#FF0000'}});
											tmp7.push({x:x[k],y:data.DHF[k][0],marker:{enabled:true,fillColor:'#FF0000'}})
										}
									}else{
										tmp.push({x:x[k],y:data.pss[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
										if(data.type==1&&c==1){
											tmp1.push({x:x[k],y:data.NHS[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp2.push({x:x[k],y:data.NHA[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp3.push({x:x[k],y:data.NHF[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp4.push({x:x[k],y:data.DHP[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp5.push({x:x[k],y:data.DHS[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp6.push({x:x[k],y:data.DHA[k][0],marker:{enabled:true,fillColor:'#FFFF00'}});
											tmp7.push({x:x[k],y:data.DHF[k][0],marker:{enabled:true,fillColor:'#FFFF00'}})
										}
									}
								}
							}
						}
					}
				}
				if(tmp.length != 0){
					pss.push(null);
					pss.push(tmp)
					if(data.type==1&&c==1){
						NHS.push(null);
						NHA.push(null);
						NHF.push(null);
						DHP.push(null);
						DHS.push(null);
						DHA.push(null);
						DHF.push(null);
						NHS.push(tmp1);
						NHA.push(tmp2);
						NHF.push(tmp3);
						DHP.push(tmp4);
						DHS.push(tmp5);
						DHA.push(tmp6);
						DHF.push(tmp7);
					}
				}
				if(c==0){series.push({name:data.name,data:pss})}else{series.push({name:'Pss',data:pss})}
				if(data.type==1&&c==1){
					series.push({name:'Native_Heap(Size)',data:NHS});
					series.push({name:'Native_Heap(Alloc)',data:NHA});
					series.push({name:'Native_Heap(Free)',data:NHF});
					series.push({name:'Dalvik_Pss',data:DHP});
					series.push({name:'Dalvik_Heap(Size)',data:DHS});
					series.push({name:'Dalvik_Heap(Alloc)',data:DHA});
					series.push({name:'Dalvik_Heap(Free)',data:DHF})
				}
				pss=[];tmp=[];
				if(data.type==1&&c==1){
					NHS=[];NHA=[];NHF=[];DHP=[];DHS=[];DHA=[];DHF=[];tmp1=[];tmp2=[];tmp3=[];tmp4=[];tmp5=[];tmp6=[];tmp7=[];
				}
				pid=0;
				break
			}
		}
	}
return [lta,series];}

function getmemline(a,b,t){
	var path,data,lines=[],tmp=[];
	switch (a){
		case 1:
			path="json/hour_" + t + "/pssline.json";
			data=JSON.parse(fs.readFileSync(path));
			tmp=data.maxpss
		break;
		case 2:
			path="json/hour_" + t + "/pdline.json";
			data=JSON.parse(fs.readFileSync(path));
			tmp=data.maxPD
		break;
	}
	if(b==0||b>=tmp.length){b=tmp.length}
	if(b>0){for (var i=0; i < b; i++) {lines.push(tmp[i][0])}}
	if(b==-1){lines=tmp}
return lines;}