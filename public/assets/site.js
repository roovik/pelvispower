(function(){try{if(localStorage.getItem('pp18')==='1')return}catch(e){}
var g=document.getElementById('agegate');if(!g)return;g.hidden=false;
document.getElementById('yes').onclick=function(){try{localStorage.setItem('pp18','1')}catch(e){}g.hidden=true}})();
