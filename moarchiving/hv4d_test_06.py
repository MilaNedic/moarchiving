from hv_plus import setup_cdllist, preprocessing, hv4dplusR

points = [
0.0055, 0.0740, 0.0254, 0.0636,
0.0314, 0.0770, 0.0344, 0.1079,
0.0746, 0.1849, 0.0452, 0.1159,
0.0885, 0.1866, 0.1196, 0.1612,
0.1220, 0.1960, 0.1409, 0.1987,
0.2288, 0.2493, 0.2898, 0.3253,
0.2588, 0.2713, 0.3117, 0.3568,
0.2809, 0.3252, 0.3144, 0.4938,
0.3110, 0.4275, 0.3309, 0.5086,
0.3887, 0.4722, 0.3585, 0.5201,
0.5227, 0.4952, 0.4104, 0.5393,
0.5467, 0.5427, 0.5979, 0.6376,
0.7608, 0.5613, 0.6334, 0.7132,
0.7713, 0.6233, 0.7069, 0.7290,
0.8037, 0.6364, 0.7296, 0.7556,
0.8631, 0.6625, 0.7710, 0.7751,
0.8872, 0.8081, 0.7722, 0.8022,
0.9076, 0.8155, 0.8287, 0.8715,
0.9297, 0.8948, 0.8926, 0.9093,
0.9395, 0.9869, 0.9696, 0.9219
]

d = 4
ref = [1, 1, 1, 1]
n = int(len(points)/d)
head = setup_cdllist(points, n, d, ref)
preprocessing(head, d)
print("Hypervolume in 4-D:", hv4dplusR(head))