(() => {
  'use strict';
  const prayers={fajr:{name:'Sabah',rakats:2},dhuhr:{name:'Öğle',rakats:4},asr:{name:'İkindi',rakats:4},maghrib:{name:'Akşam',rakats:3},isha:{name:'Yatsı',rakats:4},witr:{name:'Vitir',rakats:3}};
  const $=id=>document.getElementById(id);
  const fmt=n=>new Intl.NumberFormat('tr-TR').format(Math.max(0,Math.round(n)));
  const DAY=86400000;

  function parseLocalDate(value){
    if(!value) return null;
    const d=new Date(value+'T00:00:00');
    return Number.isNaN(d.getTime())?null:d;
  }
  function durationLabel(days){
    const years=Math.floor(days/365.2425),months=Math.floor((days-years*365.2425)/30.44),remain=Math.max(0,Math.round(days-years*365.2425-months*30.44));
    return [years?years+' yıl':'',months?months+' ay':'',remain?remain+' gün':''].filter(Boolean).join(' ')||'1 günden az';
  }
  function missingDays(){
    const birth=parseLocalDate($('birthDate').value);
    const puberty=parseLocalDate($('pubertyDate').value);
    const today=new Date(); today.setHours(0,0,0,0);
    if(!birth || !puberty) throw new Error('Doğum tarihi ve buluğ çağı tarihini girin.');
    if(puberty<birth) throw new Error('Buluğ çağı tarihi doğum tarihinden önce olamaz.');
    if(puberty>today) throw new Error('Buluğ çağı tarihi bugünden ileri olamaz.');
    const obligationDays=Math.floor((today-puberty)/DAY)+1;
    const prayedYears=Math.max(0,Math.floor(parseFloat($('prayedYears').value)||0));
    const prayedMonths=Math.max(0,Math.floor(parseFloat($('prayedMonths').value)||0));
    if(prayedMonths>11) throw new Error('Ay alanına 0 ile 11 arasında bir değer girin.');
    const prayedDays=Math.round(prayedYears*365.2425+prayedMonths*30.44);
    if(prayedDays>obligationDays) throw new Error('Kıldığınız namaz süresi, buluğ çağından bugüne kadar olan süreden uzun olamaz.');
    return Math.max(0,obligationDays-prayedDays);
  }
  function calculate(ev){
    ev.preventDefault();
    try{
      const days=missingDays();
      const selected=[...document.querySelectorAll('input[name="prayer"]:checked')].map(x=>x.value);
      if(!selected.length) throw new Error('En az bir vakit seçin.');
      if(!days) throw new Error('Hesaplanacak kaza namazı günü bulunamadı.');
      const daily=5;
      const total=days*selected.length;
      const rakats=selected.reduce((sum,key)=>sum+days*prayers[key].rakats,0);
      const planDays=Math.ceil(total/daily);
      const finish=new Date(); finish.setDate(finish.getDate()+planDays);
      $('totalDays').textContent=fmt(days);
      $('totalPrayers').textContent=fmt(total);
      $('totalRakats').textContent=fmt(rakats);
      $('finishDate').textContent=finish.toLocaleDateString('tr-TR',{day:'numeric',month:'long',year:'numeric'});
      $('resultSummary').textContent=`Girdiğiniz bilgilere göre yaklaşık ${fmt(days)} eksik gün ve ${fmt(total)} kaza vakti hesaplandı.`;
      $('prayerBreakdown').innerHTML=selected.map(k=>`<article><span>${prayers[k].name}</span><strong>${fmt(days)} vakit</strong><small>${fmt(days*prayers[k].rakats)} rekât</small></article>`).join('');
      $('planTitle').textContent='Günde 5 vakitlik örnek plan';
      $('planDescription').textContent=`Günde 5 kaza vakti hedefiyle teorik tamamlanma süresi ${durationLabel(planDays)} olur. Bu yalnızca yaklaşık matematiksel bir plandır.`;
      $('durationText').textContent=durationLabel(planDays);
      $('resultSection').hidden=false;
      $('resultSection').scrollIntoView({behavior:'smooth',block:'start'});
      window.__lastResult={days,total,rakats,daily,finish:$('finishDate').textContent};
    }catch(err){ alert(err.message); }
  }
  $('calculatorForm')?.addEventListener('submit',calculate);
  $('printButton')?.addEventListener('click',()=>window.print());
  $('copyButton')?.addEventListener('click',async()=>{
    const r=window.__lastResult;if(!r)return;
    const text=`Kaza namazı yaklaşık hesabım: ${fmt(r.days)} eksik gün, ${fmt(r.total)} vakit, ${fmt(r.rakats)} rekât. Tahmini bitiş: ${r.finish}.`;
    try{await navigator.clipboard.writeText(text);$('copyButton').textContent='Kopyalandı';setTimeout(()=>$('copyButton').textContent='Sonucu kopyala',1500)}catch{alert(text)}
  });
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
