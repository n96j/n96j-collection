(function(){
  var D=window.EXTRAS||[], PAGE=100, S={c:'',q:'',n:PAGE};
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var norm=function(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'')};
  D.forEach(function(x){x.h=norm(x.t+' '+x.c)});
  var pills=document.getElementById('xpills'), list=document.getElementById('xlist'), box=document.getElementById('xbusca');
  if(!list) return;
  function short(t){return t.length>150?t.slice(0,147)+'...':t}
  function row(x){return '<li><span class="nm"><b title="'+esc(x.t)+'">'+esc(short(x.t))+'</b><br><small>'+esc(x.c)+'</small></span><span class="dl"><a class="btn sm" href="'+esc(x.u)+'" target="_blank" rel="noopener">&#11015; '+(x.f==='FOLDER'?'Open download page':'Download ('+esc(x.f)+')')+'</a></span></li>'}
  function filtered(){var w=norm(S.q).split(/\s+/).filter(Boolean);
    return D.filter(function(x){return (!S.c||x.c===S.c)&&w.every(function(y){return x.h.indexOf(y)>=0})})}
  function drawPills(){
    var cnt={};D.forEach(function(x){cnt[x.c]=(cnt[x.c]||0)+1});
    var h='<button class="pill'+(S.c?'':' on')+'" data-c="">All <i>'+D.length+'</i></button>';
    (window.XORDER||Object.keys(cnt)).forEach(function(c){if(cnt[c]) h+='<button class="pill'+(S.c===c?' on':'')+'" data-c="'+esc(c)+'">'+esc(c)+' <i>'+cnt[c]+'</i></button>'});
    pills.innerHTML=h}
  function draw(){var r=filtered();
    var h='<p><b>'+r.length+'</b> item'+(r.length==1?'':'s')+(S.q?' for &ldquo;'+esc(S.q)+'&rdquo;':'')+'</p>';
    if(!r.length) h+='<div class="vazio">Nothing found. Try fewer words or another category.</div>';
    else h+='<ul class="lista box">'+r.slice(0,S.n).map(row).join('')+'</ul>'+(r.length>S.n?'<p><button class="pill more" id="xmore">Show '+Math.min(PAGE,r.length-S.n)+' more ('+(r.length-S.n)+' left)</button></p>':'');
    list.innerHTML=h}
  pills.addEventListener('click',function(e){var b=e.target.closest('[data-c]');if(!b)return;S.c=b.dataset.c;S.n=PAGE;drawPills();draw()});
  list.addEventListener('click',function(e){if(e.target.id==='xmore'){S.n+=PAGE;draw()}});
  box.addEventListener('input',function(){S.q=box.value.trim();S.n=PAGE;draw()});
  var m=/[?&]q=([^&]*)/.exec(location.search); if(m){S.q=decodeURIComponent(m[1].replace(/\+/g,' '));box.value=S.q}
  drawPills();draw();
})();
