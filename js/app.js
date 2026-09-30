(function(){
  var D=window.BUILDS||[], S={v:null,k:null,l:'',q:''}, Q='';
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var norm=function(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'')};
  var ALIAS={'ptbr':'portuguese brazil','portugues':'portuguese','pt-br':'portuguese brazil','win':'windows','seven':'7','eight':'8','ingles':'english','espanol':'spanish','64':'64-bit','32':'32-bit','x64':'64-bit','x86':'32-bit','x32':'32-bit','iso':'iso'};
  D.forEach(function(b){b.h=norm([b.t,b.v,b.k,b.l,b.o].join(' '))});
  function btns(b,cls){return b.d.map(function(d){
    var txt=d[2]==='FOLDER'?'Open download page':'Download'+(d[0]?' '+d[0]:'')+(d[2]?' ('+d[2]+')':'');
    if(b.d.length>1&&d[2]!=='FOLDER') txt='Download '+(d[0]||d[2])+' ('+d[2]+')';
    return '<a class="btn '+(cls||'')+'" href="'+esc(d[1])+'" target="_blank" rel="noopener">&#11015; '+esc(txt)+'</a>'}).join(' ')}
  function row(b){return '<li><span class="nm"><b>'+esc(b.t)+'</b><br><small>'+esc(b.v)+' &middot; '+esc(b.k)+'</small></span><span class="dl">'+btns(b,'sm')+'</span></li>'}
  function search(q){var w=norm(q).split(/\s+/).filter(Boolean).map(function(x){return ALIAS[x]||x});
    return D.filter(function(b){return w.every(function(x){return x.split(' ').every(function(y){return b.h.indexOf(y)>=0})})})}
  var root=document.getElementById('wizard'), box=document.getElementById('busca');
  if(!root) return;
  function counts(list,key){var m={};list.forEach(function(b){m[b[key]]=(m[b[key]]||0)+1});return m}
  function pick(label,n,attr,val){return '<button class="pick" data-'+attr+'="'+esc(val)+'"><span>'+esc(label)+'</span><i>'+n+'</i></button>'}
  function crumbs(){var h='<a data-go="0">All versions</a>';
    if(S.v) h+=' &rsaquo; <a data-go="1">'+esc(S.v)+'</a>'; if(S.k) h+=' &rsaquo; <b>'+esc(S.k)+'</b>';
    return '<div class="crumbs">'+h+'</div>'}
  var HELP={'Official release':'Final versions, service packs and retail ISOs.','Beta / Pre-release':'Betas, previews, leaks and development builds.','Modded / Lite (unofficial)':'Fan-made, trimmed or customized versions.','Extras (Service Packs, DDK, symbols)':'Service packs, rollups, DDKs, debug symbols and boot disks for this Windows.','Unverified (check before using)':'Odd or unclear items. Not confirmed to be what the title says, so check the page first.'};
  var KINDS=['Official release','Beta / Pre-release','Modded / Lite (unofficial)','Extras (Service Packs, DDK, symbols)','Unverified (check before using)'];
  function lst(l){var w=norm(S.q).split(/\s+/).filter(Boolean);var f=l.filter(function(b){return (!S.l||b.l===S.l)&&w.every(function(x){return b.h.indexOf(x)>=0})});return f.map(row).join('')||'<li>Nothing here. Try another language or filter.</li>'}
  function render(){var h='';
    if(Q){var r=search(Q);
      h='<p><b>'+r.length+'</b> result'+(r.length==1?'':'s')+' for &ldquo;'+esc(Q)+'&rdquo;</p><ul class="lista box">'+r.slice(0,150).map(row).join('')+'</ul>'+(r.length>150?'<p class="cap">Showing 150 of '+r.length+'. Type more words to narrow it down.</p>':'');
    } else if(!S.v){
      var c=counts(D,'v'); h='<span class="step">Step 1 of 2</span><h2>Which Windows do you want?</h2>';
      (window.ORDER||Object.keys(c)).forEach(function(v){if(c[v]) h+=pick(v,c[v]+' downloads','v',v)});
    } else if(!S.k){
      var l=D.filter(function(b){return b.v===S.v}), c=counts(l,'k'), ks=Object.keys(c);
      if(ks.length===1){S.k=ks[0];return render()}
      h=crumbs()+'<span class="step">Step 2 of 2</span><h2>What kind of download?</h2>';
      KINDS.forEach(function(k){if(c[k]) h+=pick(k,c[k],'k',k).replace('</span>','<br><small>'+HELP[k]+'</small></span>')});
    } else {
      var l=D.filter(function(b){return b.v===S.v&&b.k===S.k}), lc=counts(l,'l'), ln=Object.keys(lc).sort(function(a,b){return a==='English'?-1:b==='English'?1:a<b?-1:1});
      h=crumbs()+'<div class="filtros"><label>Language <select id="fl"><option value="">All ('+l.length+')</option>'+ln.map(function(x){return '<option'+(x===S.l?' selected':'')+' value="'+esc(x)+'">'+esc(x)+' ('+lc[x]+')</option>'}).join('')+'</select></label><input id="fq" type="search" placeholder="Filter this list: 22H2, SP1, ultimate..." value="'+esc(S.q)+'"></div>';
      h+='<ul class="lista box" id="lst">'+lst(l)+'</ul>';
    }
    root.innerHTML=h;}
  root.addEventListener('click',function(e){var t=e.target.closest('[data-v],[data-k],[data-go]'); if(!t) return;
    if(t.dataset.v!==undefined){S.v=t.dataset.v;S.l='';S.q=''} else if(t.dataset.k!==undefined) S.k=t.dataset.k;
    else {var g=+t.dataset.go; if(g<2) S.k=null; if(g<1) S.v=null; S.l='';S.q=''}
    render(); window.scrollTo(0,0)});
  root.addEventListener('input',function(e){if(e.target.id==='fq'){S.q=e.target.value;document.getElementById('lst').innerHTML=lst(D.filter(function(b){return b.v===S.v&&b.k===S.k}))}});
  root.addEventListener('change',function(e){if(e.target.id==='fl'){S.l=e.target.value;render()}});
  box.addEventListener('input',function(e){Q=e.target.value.trim();render()});
  var m=/[?&]q=([^&]*)/.exec(location.search); if(m){Q=decodeURIComponent(m[1].replace(/\+/g,' '));box.value=Q}
  render();
})();
