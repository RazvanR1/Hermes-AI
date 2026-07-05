import type { ReactNode } from "react";

export default function PageContainer({

children

}:{

children:ReactNode

}){

return(

<div className="mx-auto max-w-[1700px] p-8">

{children}

</div>

);

}
