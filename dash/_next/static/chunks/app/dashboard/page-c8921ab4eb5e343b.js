(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[702],{9619:function(e,t,r){Promise.resolve().then(r.bind(r,7252))},5100:function(e,t,r){"use strict";r.d(t,{I:function(){return i},W:function(){return AppStateProvider}});var a=r(7437),s=r(2265);let n={title:"GOI Budget 2023-24",selected_csv:"/dash/data/goi2324/goi.csv"};function AppStateReducer(e,t){switch(t.type){case"RESET":return n;case"SET_TITLE":return{...e,title:t.title};case"SET_CSV":return{...e,selected_csv:t.csv};case"SET_TITLE_AND_CSV":let r="/dash/data/goi2324/".concat(t.csv,".csv");return{...e,title:t.title,selected_csv:r};default:return e}}let i=(0,s.createContext)({state:n,dispatch:()=>{}}),AppStateProvider=e=>{let{children:t}=e,[r,d]=(0,s.useReducer)(AppStateReducer,n);return(0,a.jsx)(i.Provider,{value:{state:r,dispatch:d},children:t})}},5886:function(e,t,r){"use strict";var a=r(1812),s=r.n(a);let CsvReader=class CsvReader{async read(e){let t=await fetch(e),r=await t.text(),a=s().parse(r,{header:!0}),n=[];for(let e of a.data)n.push({source_name:e.source_name,dest_name:e.dest_name,source_abbrev:e.source_abbrev,dest_abbrev:e.dest_abbrev,amount:e.amount,amount_inr:e.amount_inr,amount_usd:e.amount_usd});return n}async get_dno_edges(e){console.log("Loading URL: ",e);let t=await this.read(e),r={};for(let e of t){let t=e.source_abbrev,a=e.dest_abbrev,s=e.amount_usd;r[t]=(r[t]||0)+Number(s),r[a]=(r[a]||0)+Number(s)}let a=t.filter(e=>{let t=e.source_abbrev,a=e.dest_abbrev;return r[t],r[a]>4e8});return a.length<8&&(a=t),{parents:a.map(e=>e.source_abbrev),ids:a.map(e=>e.dest_abbrev),labels:a.map(e=>e.dest_name),values:a.map(e=>e.amount_usd/1e9)}}async read_dir(){return[]}constructor(){}};t.Z=CsvReader},7252:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return Page}});var a=r(7437),s=r(2265),n=r(3857),i=r(6500),d=r(4989),l=r(8938),o=r(2653),u=r(8874),c=r(6055),m=r(3226),h=r(5100),_=r(5886),b=r(1709),v=r(9042),x=r(6921),f=r(7543),p=r(4368),g=r(2750),j=r(8075);let w=[{field:"id",headerName:"ID",width:150},{field:"source_abbrev",headerName:"srckey",width:150},{field:"source_name",headerName:"srcname",width:150},{field:"dest_abbrev",headerName:"destkey",width:150},{field:"dest_name",headerName:"Ministry/Department",width:450},{field:"amount",headerName:"Amount",width:150},{field:"amount_inr",headerName:"Amount_INR",width:150},{field:"amount_usd",type:"number",headerName:"Amount (USD, $)",width:150,valueFormatter:e=>{if(null==e.value)return"";let t=e.value/1e9,r=t.toFixed(2);return"$".concat(r,"B")}}];function CustomGridToolbar(){return(0,a.jsxs)(b.D,{children:[(0,a.jsx)(v.S,{}),(0,a.jsx)(x.M,{}),(0,a.jsx)(f.L,{}),(0,a.jsx)(p.Zh,{}),(0,a.jsx)(g.T,{})]})}var BudgetDataGrid=()=>{let[e,t]=s.useState([]),{state:r,dispatch:n}=(0,s.useContext)(h.I);return(s.useEffect(()=>{let e=new _.Z;e.read(r.selected_csv).then(e=>{let r=e.map((e,t)=>(e.id=t,e));t(r)})},[r.selected_csv]),0==e.length)?(0,a.jsx)("div",{children:"Loading..."}):(0,a.jsx)("div",{style:{height:400},children:(0,a.jsx)(j._$,{filterMode:"client",initialState:{columns:{columnVisibilityModel:{id:!1,source_abbrev:!1,dest_abbrev:!1,amount:!1,amount_inr:!1}},sorting:{sortModel:[{field:"amount_usd",sort:"desc"}]},filter:{filterModel:{items:[],quickFilterValues:[""]}},pagination:{paginationModel:{pageSize:10}}},slots:{toolbar:CustomGridToolbar},rows:e,columns:w,onRowClick:e=>{let t=e.row.dest_abbrev,r=e.row.dest_name,a=t.replace("g2_","");console.log("Changing to: ",a),n({type:"SET_TITLE_AND_CSV",title:r,csv:a})}})})},S=r(2303),N=r(8811),C=r.n(N);let E=C()(()=>Promise.all([r.e(934),r.e(609)]).then(r.bind(r,305)).then(e=>e.default),{loadableGenerated:{webpack:()=>[305]},ssr:!1});function Page(){let{state:e,dispatch:t}=(0,s.useContext)(h.I);return(0,a.jsxs)("div",{children:[(0,a.jsx)(n.ZP,{}),(0,a.jsx)(i.Z,{position:"static",children:(0,a.jsxs)(d.Z,{children:[(0,a.jsx)(o.Z,{size:"large",edge:"start",color:"inherit","aria-label":"go-home",sx:{mr:2},onClick:()=>{t({type:"RESET"})},children:(0,a.jsx)(S.Z,{})}),(0,a.jsx)(m.Z,{variant:"h5",component:"div",sx:{flexGrow:1},children:e.title})]})}),(0,a.jsx)(l.Z,{maxWidth:"xl",sx:{mt:1,mb:0},children:(0,a.jsxs)(u.ZP,{container:!0,spacing:3,columnSpacing:0,sx:{p:0},children:[(0,a.jsx)(u.ZP,{item:!0,xs:12,md:8,lg:12,children:(0,a.jsx)(c.Z,{sx:{p:0,display:"flex",flexDirection:"column",height:720},children:(0,a.jsx)(E,{})})}),(0,a.jsx)(u.ZP,{item:!0,xs:12,children:(0,a.jsx)(c.Z,{sx:{p:2,display:"flex",flexDirection:"column"},children:(0,a.jsx)(BudgetDataGrid,{})})})]})})]})}}},function(e){e.O(0,[771,971,472,744],function(){return e(e.s=9619)}),_N_E=e.O()}]);