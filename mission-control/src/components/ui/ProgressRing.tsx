type Props={

value:number

size?:number

};

export default function ProgressRing({

value,

size=170

}:Props){

const stroke=12;

const radius=(size-stroke)/2;

const circumference=2*Math.PI*radius;

const offset=circumference-(value/100)*circumference;

return(

<svg width={size} height={size}>

<circle

cx={size/2}

cy={size/2}

r={radius}

stroke="#233042"

strokeWidth={stroke}

fill="none"

/>

<circle

cx={size/2}

cy={size/2}

r={radius}

stroke="#22d3ee"

strokeWidth={stroke}

strokeLinecap="round"

fill="none"

strokeDasharray={circumference}

strokeDashoffset={offset}

transform={`rotate(-90 ${size/2} ${size/2})`}

/>

<text

x="50%"

y="50%"

textAnchor="middle"

dy=".35em"

fontSize="30"

fill="white"

>

{value}%

</text>

</svg>

);

}
