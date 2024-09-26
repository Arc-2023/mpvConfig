##倍帧，转8bit，低开销（高于32帧的源自动忽略）

import vapoursynth as vs
core = vs.core
clip = video_in

dst_fps = display_fps
# Interpolating to fps higher than 60 is too CPU-expensive, smoothmotion can handle the rest.

# Skip interpolation for >1080p or 60 Hz content due to performance
dst_fps_num =container_fps*2
dst_fps_den = 1
# Needed because clip FPS is missing
clip = core.std.AssumeFPS(clip, fpsnum = container_fps, fpsden = 1)
sup  = core.mv.Super(clip, pel=4,rfilter=4)
bvec = core.mv.Analyse(sup,32,16,0,3,0,3, True,0,lsad=20000,badrange=0,badsad=10000,dct=0,search_coarse=4,)
fvec = core.mv.Analyse(sup,32,16,0,3,0,3, False,0,lsad=20000,badrange=0,badsad=10000,dct=0,search_coarse=4,)
#clip = core.mv.BlockFPS(clip, sup, bvec, fvec, num=dst_fps_num, den=dst_fps_den, mode=3, thscd2=12)
clip = core.mv.BlockFPS(clip, sup, bvec, fvec, dst_fps_num, dst_fps_den, mode=4, blend=False,)
clip.set_output()