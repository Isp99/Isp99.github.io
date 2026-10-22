(() => {
 "use strict";
 const opener=document.getElementById("open-study-search"),overlay=document.getElementById("note-search-overlay");
 const dialog=document.getElementById("note-search-dialog"),input=document.getElementById("note-search-input"),list=document.getElementById("note-search-results");
 const feedback=document.getElementById("note-search-feedback"),suggest=document.getElementById("note-search-suggestions"),closer=document.getElementById("close-study-search");
 const resume=document.getElementById("continue-reading");
 if(!opener||!overlay||!input||!list)return;
 let items=null,loading=null,selected=-1,matches=[],lastFocus=null;
 const storageKey="engineeringNotebook.lastStudy.v1";
 function restoreLastPage(){
   try {
     const v=JSON.parse(localStorage.getItem(storageKey)||"null");
     if(!v||typeof v.path!=="string"||!/^study\/[a-z0-9/_-]+\.html$/i.test(v.path)||v.path.includes("//"))return;
     resume.href=v.path;resume.title="Resume: "+String(v.title||"Study Note");
     resume.setAttribute("aria-label","Continue reading "+String(v.title||"your last note"));
   }catch(_){}
 }
 const lower=s=>String(s||"").toLocaleLowerCase();
 function score(doc,q,terms){
   const title=lower(doc.title),desc=lower(doc.description),group=lower(doc.group),words=lower(doc.keywords);
   if(!terms.every(t=>(title+" "+desc+" "+group+" "+words).includes(t)))return -1;
   let n=(title===q?130:0)+(title.startsWith(q)?80:0)+(title.includes(q)?55:0)+(desc.includes(q)?18:0);
   for(const t of terms)n+=(title.includes(t)?25:0)+(desc.includes(t)?10:0)+(group.includes(t)?6:0)+(words.includes(t)?2:0);
   return n-(doc.pending?3:0);
 }
 function active(){
   Array.from(list.children).forEach((el,i)=>el.classList.toggle("is-active",i===selected));
   if(selected>=0){list.children[selected]?.scrollIntoView({block:"nearest"});input.setAttribute("aria-activedescendant","note-search-result-"+selected);}
   else input.removeAttribute("aria-activedescendant");
 }
 function result(doc,i){
   const li=document.createElement("li");li.className="study-search-result";li.id="note-search-result-"+i;
   const link=document.createElement("a");link.href=doc.url;
   const main=document.createElement("span");main.className="study-search-result-main";
   const group=document.createElement("span");group.className="study-search-result-category";group.textContent=doc.group;
   const title=document.createElement("strong");title.className="study-search-result-title";title.textContent=doc.title;
   const desc=document.createElement("span");desc.className="study-search-result-desc";desc.textContent=doc.description;
   main.append(group,title,desc);
   if(doc.pending){const p=document.createElement("span");p.className="study-search-result-pending";p.textContent="In preparation";main.append(p);}
   const arrow=document.createElement("span");arrow.className="study-search-result-arrow";arrow.setAttribute("aria-hidden","true");arrow.textContent="↗";
   link.append(main,arrow);li.append(link);return li;
 }
 function render(){
   const q=lower(input.value.trim());selected=-1;matches=[];list.replaceChildren();input.removeAttribute("aria-activedescendant");
   suggest.hidden=!!q;
   if(!q){feedback.textContent="Type a keyword or choose a suggested topic.";return;}
   if(!items){feedback.textContent="Loading study notes…";return;}
   const terms=q.split(/\s+/).filter(Boolean);
   matches=items.map(doc=>({doc,n:score(doc,q,terms)})).filter(x=>x.n>=0).sort((a,b)=>b.n-a.n||a.doc.title.localeCompare(b.doc.title)).slice(0,10).map(x=>x.doc);
   matches.forEach((doc,i)=>list.append(result(doc,i)));
   feedback.textContent=matches.length?matches.length+(matches.length===10?"+ results":" matching pages"):"No matching pages. Try another keyword.";
 }
 async function load(){
   if(items)return;
   if(!loading)loading=fetch("assets/search-index.json?v=20261022-search1").then(r=>{if(!r.ok)throw Error("Cannot load index");return r.json();}).then(data=>{if(!Array.isArray(data))throw Error("Invalid index");items=data;}).catch(e=>{loading=null;throw e;});
   return loading;
 }
 async function open(){
   if(!overlay.hidden)return;lastFocus=document.activeElement;overlay.hidden=false;document.body.classList.add("study-search-open");
   input.value="";render();input.focus();
   try{await load();if(!overlay.hidden)render();}catch(_){feedback.textContent="Search is unavailable. Please retry.";}
 }
 function close(){overlay.hidden=true;document.body.classList.remove("study-search-open");lastFocus?.focus?.();}
 opener.addEventListener("click",open);closer.addEventListener("click",close);
 overlay.addEventListener("mousedown",e=>{if(e.target===overlay)close();});
 input.addEventListener("input",render);
 suggest.addEventListener("click",e=>{const b=e.target.closest("[data-search-term]");if(!b)return;input.value=b.dataset.searchTerm;render();input.focus();});
 document.addEventListener("keydown",e=>{
   if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==="k"){e.preventDefault();overlay.hidden?open():input.focus();return;}
   if(overlay.hidden)return;
   if(e.key==="Escape"){e.preventDefault();close();return;}
   if(e.key==="Tab"){
     const fs=Array.from(dialog.querySelectorAll("button:not([disabled]),input:not([disabled]),a[href]")).filter(x=>x.getClientRects().length);
     if(e.shiftKey&&document.activeElement===fs[0]){e.preventDefault();fs[fs.length-1]?.focus();}
     if(!e.shiftKey&&document.activeElement===fs[fs.length-1]){e.preventDefault();fs[0]?.focus();}
     return;
   }
   if(document.activeElement!==input||!matches.length)return;
   if(e.key==="ArrowDown"){e.preventDefault();selected=(selected+1)%matches.length;active();}
   else if(e.key==="ArrowUp"){e.preventDefault();selected=selected<=0?matches.length-1:selected-1;active();}
   else if(e.key==="Enter"){e.preventDefault();location.assign(matches[selected<0?0:selected].url);}
 });
 restoreLastPage();window.addEventListener("pageshow",restoreLastPage);
})();