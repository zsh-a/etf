
#set text(
    font: "Noto Serif CJK SC",
    // size: 11.5pt,
)


// - item 1
//    - item 1.1
//      - item 1.1.1
//  - item 2

// #table(
//   columns: (auto, auto),
//   inset: 10pt,
//   align: horizon,
//   [*Area*], [*Parameters*], 
//   $ pi h (D^2 - d^2) / 4 $, [$h$: height], 
//   $ sqrt(2) / 12 a^3 $,[$a$: edge length]
// )

// #let i = 1
// #while i <= 9 {
//     let j = 1
//     while j <= i {
//         [$#j times #i = #{j * i}$,]
//         j += 1
//     }
//     linebreak()
//     i +=1
// }

// - env
//     - Pytorch version	: 1.13.1+cu117
//     - CUDA version	: 11.7
//     - GPU		: NVIDIA GeForce RTX 4090


// n=128	n=512	n=2048	n=8192
// torch.float32	0.087	14.661	55.080	53.084
// torch.float16	0.217	12.182	161.477	155.405

// 	n=128	n=512	n=2048	n=8192
// torch.float32	0.091	18.821	54.596	53.562
// torch.float16	0.093	5.316	162.534	154.792
// #table(
//   columns: (auto, auto),
//   inset: 10pt,
//   align: horizon,
//   [*Area*], [*Parameters*], 
//   $ pi h (D^2 - d^2) / 4 $, [$h$: height], 
//   $ sqrt(2) / 12 a^3 $,[$a$: edge length]
// )

// #table(
//   columns: (auto, auto,auto,auto,auto),
// //   inset: 10pt,
//   align:horizon,
//   [], [*65536*],[*262144*],[*1048576*],[*4194304*],
//   [*TFLOPS*],[0.006],[0.021],[0.086],[0.364],
//   [*GB/s*],[45.677],[168.153],[685.798],[2912.961]

// )

// 	65536	262144	1048576	4194304
// TFLOPS	0.006	0.021	0.086	0.364
// GB/s	45.677	168.153	685.798	2912.961

// 	65536	262144	1048576	4194304
// TFLOPS	0.006	0.022	0.094	0.363
// GB/s	46.102	179.372	755.677	2902.253


// 	batch=2	batch=4	batch=8	batch=16	batch=32	batch=64	batch=128
// fwd seq_len=128	6.628	13.249	27.315	49.754	106.258	104.997	92.228
// fwd+bwd seq_len=128	7.414	13.605	30.078	53.225	102.015	112.967	91.624
// fwd seq_len=512	27.233	50.294	69.160	68.255	67.910	65.332	62.718
// fwd+bwd seq_len=512	27.110	53.873	75.578	77.068	71.538	71.420	71.098


