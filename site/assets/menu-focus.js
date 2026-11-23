
document.addEventListener('keydown',event=>{
 const sidebar=document.getElementById('sidebar');
 if(event.key==='Escape' && sidebar?.classList.contains('open')){
   document.querySelector('.menu-button')?.focus();
 }
},true);
