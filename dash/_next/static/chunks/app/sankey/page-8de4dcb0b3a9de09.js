(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[94],{5758:function(e,t,n){Promise.resolve().then(n.bind(n,6628))},5100:function(e,t,n){"use strict";n.d(t,{I:function(){return i},W:function(){return AppStateProvider}});var r=n(7437),s=n(2265);let c={key:0,title:"GOI Budget 2023-24",selected_csv:"/dash/data/goi2324.v2/goi.csv"};function AppStateReducer(e,t){switch(t.type){case"REFRESH":return{...e,key:e.key+1};case"RESET":return c;case"SET_TITLE":return{...e,title:t.title};case"SET_CSV":return{...e,selected_csv:t.csv};case"SET_TITLE_AND_CSV":let n="/dash/data/goi2324.v2/".concat(t.csv,".csv");return{...e,title:t.title,selected_csv:n};default:return e}}let i=(0,s.createContext)({state:c,dispatch:()=>{}}),AppStateProvider=e=>{let{children:t}=e,[n,l]=(0,s.useReducer)(AppStateReducer,c);return(0,r.jsx)(i.Provider,{value:{state:n,dispatch:l},children:t})}},6628:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return Page}});var r=n(7437),s=n(2265),c=n(3857),i=n(8938),l=n(9050),a=n(8874),u=n(6055),d=n(5100),o=n(8811),h=n.n(o);let x=h()(()=>Promise.all([n.e(934),n.e(901),n.e(387),n.e(26)]).then(n.bind(n,9026)).then(e=>e.default),{loadableGenerated:{webpack:()=>[9026]},ssr:!1});function Page(){let{state:e,dispatch:t}=(0,s.useContext)(d.I);return(0,r.jsxs)("div",{children:[(0,r.jsx)(c.ZP,{}),(0,r.jsxs)(i.Z,{maxWidth:"xl",sx:{mt:1,mb:0},children:[(0,r.jsx)(a.ZP,{children:(0,r.jsx)(a.ZP,{item:!0,xs:12,children:(0,r.jsx)(l.Z,{onClick:()=>{t({type:"REFRESH"})},children:"Refresh"})})}),(0,r.jsx)(a.ZP,{container:!0,spacing:3,columnSpacing:0,sx:{p:0},children:(0,r.jsx)(a.ZP,{item:!0,xs:12,md:8,lg:12,children:(0,r.jsx)(u.Z,{sx:{p:0,display:"flex",flexDirection:"column",height:1800},children:(0,r.jsx)(x,{})})})})]})]})}}},function(e){e.O(0,[979,666,971,472,744],function(){return e(e.s=5758)}),_N_E=e.O()}]);