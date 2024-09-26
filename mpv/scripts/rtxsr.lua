-- rtxsr.lua
local mp = require 'mp'

local filter_enabled = false
-- 显示器长边分辨率，大了mpv会自动降回去，参考mpv.conf的dscale参数
local max_width = 2560
-- 获取视频分辨率并计算缩放比例
local function get_scale()
    local width = mp.get_property_native("width")
    local height = mp.get_property_native("height")
    if width and height then
        local ratio = max_width / math.max(width, height)
        return ratio
    else
        return 1.0 -- 默认缩放比例
    end
end


function toggle_filter()
    if filter_enabled then
        mp.command("vf remove @rtxsr")
        filter_enabled = false
        mp.osd_message("NVIDIA Scaling: OFF")
    else
        local scale = get_scale()
        local success = mp.command(string.format("vf append @rtxsr:d3d11vpp=scale=%.2f:scaling-mode=nvidia", scale))
        if success then
            filter_enabled = true
            mp.osd_message("NVIDIA Scaling: ON")
        else
            mp.osd_message("Failed to apply NVIDIA Scaling")
        end
    end
end

mp.add_key_binding("n", "toggle-nvidia-scaling", toggle_filter)