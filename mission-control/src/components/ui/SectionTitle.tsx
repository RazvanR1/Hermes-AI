export default function SectionTitle({

title,

subtitle

}:{

title:string

subtitle?:string

}){

return(

<div className="mb-5">

<h2 className="text-xl font-bold">

{title}

</h2>

{subtitle&&(

<p className="text-slate-400 text-sm">

{subtitle}

</p>

)}

</div>

);

}
