import type { ReactNode } from "react";

export default function Card({

children,

className=""

}:{

children:ReactNode

className?:string

}){

return(

<div

className={

"rounded-2xl border border-slate-700 bg-slate-900/70 backdrop-blur-lg shadow-xl p-5 "+className

}

>

{children}

</div>

);

}
