export default function StatusBadge({

status

}:{

status:string

}){

const map:any={

healthy:"bg-green-500",

online:"bg-green-500",

warning:"bg-amber-500",

critical:"bg-red-500",

offline:"bg-red-500"

};

return(

<div className="flex items-center gap-2">

<div className={`w-3 h-3 rounded-full ${map[status]||"bg-slate-500"}`} />

<span className="text-sm capitalize">{status}</span>

</div>

);

}
