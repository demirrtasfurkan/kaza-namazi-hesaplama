(() => {
  'use strict';
  const prayers={fajr:{name:'Sabah',rakats:2},dhuhr:{name:'Öğle',rakats:4},asr:{name:'İkindi',rakats:4},maghrib:{name:'Akşam',rakats:3},isha:{name:'Yatsı',rakats:4},witr:{name:'Vitir',rakats:3}};
  const $=id=>document.getElementById(id); const fmt=n=>new Intl.NumberFormat('tr-TR').format(Math.max(0,Math.round(n))); const method=$('method');
  function switchMethod(){['years','days','date'].forEach(x=>{const el=$(x+'Fields');if(el)el.hidden=true});const id=method.value==='dates'?'dateFields':method.value+'Fields';$(id).hidden=false;}
  document.querySelectorAll('input[name="methodChoice"]').forEach(r=>r.addEventListener('change',()=>{method.value=r.value;switchMethod()}));
  document.querySelectorAll('[data-target]').forEach(b=>b.addEventListener('click',()=>{$('dailyTarget').value=b.dataset.target;document.querySelectorAll('[data-target]').forEach(x=>x.classList.toggle('is-active',x===b));}));$('dailyTarget').addEventListener('input',()=>{document.querySelectorAll('[data-target]').forEach(b=>b.classList.toggle('is-active',b.dataset.target===$('dailyTarget').value));});
  const params=new URLSearchParams(location.search);if(params.has('years')){$('years').value=params.get('years');method.value='years';document.querySelector('input[name="methodChoice"][value="years"]').checked=true}switchMethod();
  function baseDays(){if(method.value==='years')return Math.round((parseFloat($('years').value)||0)*365.2425);if(method.value==='days')return Math.round(parseFloat($('days').value)||0);const s=new Date($('startDate').value),e=new Date($('endDate').value);if(Number.isNaN(s.getTime())||Number.isNaN(e.getTime())||e<s)throw new Error('Geçerli bir başlangıç ve bitiş tarihi girin.');return Math.floor((e-s)/86400000)+1}
  function durationLabel(days){const years=Math.floor(days/365.2425),months=Math.floor((days-years*365.2425)/30.44),remain=Math.max(0,Math.round(days-years*365.2425-months*30.44));return[years?years+' yıl':'',months?months+' ay':'',remain?remain+' gün':''].filter(Boolean).join(' ')||'1 günden az'}
  function calculate(ev){ev.preventDefault();try{const excluded=Math.max(0,Math.round(parseFloat($('excludedDays').value)||0)),days=Math.max(0,baseDays()-excluded),selected=[...document.querySelectorAll('input[name="prayer"]:checked')].map(x=>x.value);if(!selected.length)throw new Error('En az bir vakit seçin.');if(!days)throw new Error('Hesaplanacak eksik gün bulunamadı.');const daily=Math.max(1,Math.round(parseFloat($('dailyTarget').value)||1)),total=days*selected.length,rakats=selected.reduce((s,k)=>s+days*prayers[k].rakats,0),planDays=Math.ceil(total/daily),finish=new Date();finish.setDate(finish.getDate()+planDays);$('totalDays').textContent=fmt(days);$('totalPrayers').textContent=fmt(total);$('totalRakats').textContent=fmt(rakats);$('finishDate').textContent=finish.toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'});$('resultSummary').textContent=`Seçtiğiniz bilgilere göre yaklaşık ${fmt(days)} eksik gün ve ${fmt(total)} vakit hesaplandı.`;$('prayerBreakdown').innerHTML=selected.map(k=>`<article><span>${prayers[k].name}</span><strong>${fmt(days)} vakit</strong><small>${fmt(days*prayers[k].rakats)} rekât</small></article>`).join('');$('planTitle').textContent=`Günde ${fmt(daily)} vakitlik plan`;$('planDescription').textContent=`Bu hedef korunursa toplam borcun teorik olarak ${durationLabel(planDays)} içinde tamamlanması beklenir. Günlük farz namazlar bu hedefe dahil değildir.`;$('durationText').textContent=durationLabel(planDays);$('resultSection').hidden=false;$('resultSection').scrollIntoView({behavior:'smooth',block:'start'});window.__lastResult={days,total,rakats,daily,finish:$('finishDate').textContent}}catch(err){alert(err.message)}}
  $('calculatorForm').addEventListener('submit',calculate);$('printButton').addEventListener('click',()=>window.print());$('copyButton').addEventListener('click',async()=>{const r=window.__lastResult;if(!r)return;const text=`Kaza namazı yaklaşık planım: ${fmt(r.days)} eksik gün, ${fmt(r.total)} vakit, ${fmt(r.rakats)} rekât. Günlük hedef: ${fmt(r.daily)} vakit. Tahmini bitiş: ${r.finish}.`;try{await navigator.clipboard.writeText(text);$('copyButton').textContent='Kopyalandı';setTimeout(()=>$('copyButton').textContent='Sonucu kopyala',1500)}catch{alert(text)}});
})();

// Haftalık takip çizelgesi: CSP nedeniyle inline onclick yerine harici JS kullanılır.
(() => {
  'use strict';
  const printButton = document.getElementById('printTrackerButton');
  const clearButton = document.getElementById('clearTrackerButton');
  const status = document.getElementById('trackerStatus');
  const inputs = [...document.querySelectorAll('#cizelge .tracker-input')];

  if (printButton) {
    printButton.addEventListener('click', () => {
      if (status) status.textContent = 'Yazdırma penceresi açılıyor…';
      window.print();
      window.setTimeout(() => {
        if (status) status.textContent = '';
      }, 1500);
    });
  }

  if (clearButton) {
    clearButton.addEventListener('click', () => {
      inputs.forEach(input => { input.value = ''; });
      if (status) status.textContent = 'Çizelge temizlendi.';
      window.setTimeout(() => {
        if (status) status.textContent = '';
      }, 1500);
    });
  }
})();
