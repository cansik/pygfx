"""
THIS CODE IS AUTOGENERATED - DO NOT EDIT
"""


import os
from os import path
from cffi import FFI

from .wgpu import BaseWGPU

os.environ["RUST_BACKTRACE"] = "10"

HERE = path.dirname(path.realpath(__file__))

ffi = FFI()

# read file
lines = []
with open(path.join(HERE, 'wgpu.h')) as f:
    for line in f.readlines():
        if not line.startswith(("#include ", "#define WGPU_LOCAL", "#define WGPUColor", "#define WGPUOrigin3d_ZERO", "#if defined", "#endif")):
            lines.append(line)


# configure cffi
ffi.cdef("".join(lines))
ffi.set_source("whatnameshouldiusehere", None)

_lib = ffi.dlopen(path.join(HERE, "wgpu_native-debug.dll"))


# cffi will check the types of structs, and will also raise an error
# when setting a non-existing struct attribute. It does not check whether
# values are not set (it will simply use default values or null pointers).
# Unions are also a bit of a hassle. Therefore we include struct_info
# so we can handle "special fields" in some structs. The base API offers
# a way to create structs using a function that ensures that all fields
# are set (and making union fields optional).

def dict_to_struct(d, structname, refs):
    special_fields = _struct_info.get(structname, None)
    if not special_fields:
        return ffi.new(structname + " *", d)  # simple, flat
    s = ffi.new(structname + " *")
    for key, val in d.items():
        info = special_fields.get(key, None)
        if info:
            subtypename, is_pointer, is_optional = info
            if is_optional and val is None:
                continue
            elif val is None:
                cval = ffi.NULL
            elif isinstance(val, str):
                cval = ffi.new("char []", val.encode())
                refs.append(cval)
            elif isinstance(val, dict):
                cval = dict_to_struct(val, subtypename, refs)
                refs.append(cval)
                if not is_pointer:
                    cval = cval[0]
            elif isinstance(val, (tuple, list)):
                cval = [dict_to_struct(v, subtypename, refs) for v in val]
                refs.extend(cval)
                cval = ffi.new(subtypename + " []", [v[0] for v in cval])
                refs.append(cval)
            else:
                cval = val  # We trust the user
                # raise TypeError(f"Expected dict or list for {subtypename}")
        elif val is None:
            cval = ffi.NULL
        else:
            cval = val
        setattr(s, key, cval)
    return s


# Define what struct fields are sub-structs
_struct_info = dict(
    WGPUDeviceDescriptor = {
        'extensions': ('WGPUExtensions', False, False),
        'limits': ('WGPULimits', False, False),
    },
    WGPURenderPassColorAttachmentDescriptor = {
        'resolve_target': ('WGPUTextureViewId', True, False),
        'clear_color': ('WGPUColor', False, False),
    },
    WGPURenderPassDescriptor = {
        'color_attachments': ('WGPURenderPassColorAttachmentDescriptor', True, False),
        'depth_stencil_attachment': ('WGPURenderPassDepthStencilAttachmentDescriptor_TextureViewId', True, False),
    },
    WGPUTextureCopyView = {
        'origin': ('WGPUOrigin3d', False, False),
    },
    WGPUBindingResource_WGPUBuffer_Body = {
        '_0': ('WGPUBufferBinding', False, False),
    },
    WGPUBindingResource = {
        'buffer': ('WGPUBindingResource_WGPUBuffer_Body', False, True),
        'sampler': ('WGPUBindingResource_WGPUSampler_Body', False, True),
        'texture_view': ('WGPUBindingResource_WGPUTextureView_Body', False, True),
    },
    WGPUBindGroupBinding = {
        'resource': ('WGPUBindingResource', False, False),
    },
    WGPUBindGroupDescriptor = {
        'bindings': ('WGPUBindGroupBinding', True, False),
    },
    WGPUBindGroupLayoutDescriptor = {
        'bindings': ('WGPUBindGroupLayoutBinding', True, False),
    },
    WGPUProgrammableStageDescriptor = {
        'entry_point': ('WGPURawString', False, False),
    },
    WGPUComputePipelineDescriptor = {
        'compute_stage': ('WGPUProgrammableStageDescriptor', False, False),
    },
    WGPUPipelineLayoutDescriptor = {
        'bind_group_layouts': ('WGPUBindGroupLayoutId', True, False),
    },
    WGPUColorStateDescriptor = {
        'alpha_blend': ('WGPUBlendDescriptor', False, False),
        'color_blend': ('WGPUBlendDescriptor', False, False),
    },
    WGPUDepthStencilStateDescriptor = {
        'stencil_front': ('WGPUStencilStateFaceDescriptor', False, False),
        'stencil_back': ('WGPUStencilStateFaceDescriptor', False, False),
    },
    WGPUVertexBufferDescriptor = {
        'attributes': ('WGPUVertexAttributeDescriptor', True, False),
    },
    WGPUVertexInputDescriptor = {
        'vertex_buffers': ('WGPUVertexBufferDescriptor', True, False),
    },
    WGPURenderPipelineDescriptor = {
        'vertex_stage': ('WGPUProgrammableStageDescriptor', False, False),
        'fragment_stage': ('WGPUProgrammableStageDescriptor', True, False),
        'rasterization_state': ('WGPURasterizationStateDescriptor', True, False),
        'color_states': ('WGPUColorStateDescriptor', True, False),
        'depth_stencil_state': ('WGPUDepthStencilStateDescriptor', True, False),
        'vertex_input': ('WGPUVertexInputDescriptor', False, False),
    },
    WGPUU32Array = {
        'bytes': ('uint32_t', True, False),
    },
    WGPUShaderModuleDescriptor = {
        'code': ('WGPUU32Array', False, False),
    },
    WGPUTextureDescriptor = {
        'size': ('WGPUExtent3d', False, False),
    },
)


class RsWGPU(BaseWGPU):
    """ WebGPU API implemented using the C-API dll of wgpu-rs, via cffi.
    """
    def _tostruct(self, struct_name, d):
        return d#ffi.new('WGPU' + struct_name + ' *', d)[0]

    def adapter_request_device(self, adapter_id: int, desc: 'DeviceDescriptor'):
        """
        WGPUDeviceId wgpu_adapter_request_device(WGPUAdapterId adapter_id,
                                                 const WGPUDeviceDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUDeviceDescriptor', xx)
        return _lib.wgpu_adapter_request_device(adapter_id, desc)

    def bind_group_destroy(self, bind_group_id: int):
        """
        void wgpu_bind_group_destroy(WGPUBindGroupId bind_group_id);
        """
        xx = []
        return _lib.wgpu_bind_group_destroy(bind_group_id)

    def buffer_destroy(self, buffer_id: int):
        """
        void wgpu_buffer_destroy(WGPUBufferId buffer_id);
        """
        xx = []
        return _lib.wgpu_buffer_destroy(buffer_id)

    def buffer_map_read_async(self, buffer_id: int, start: int, size: int, callback: 'BufferMapReadCallback', userdata: 'uint8'):
        """
        void wgpu_buffer_map_read_async(WGPUBufferId buffer_id,
                                        WGPUBufferAddress start,
                                        WGPUBufferAddress size,
                                        WGPUBufferMapReadCallback callback,
                                        uint8_t *userdata);
        """
        xx = []
        return _lib.wgpu_buffer_map_read_async(buffer_id, start, size, callback, userdata)

    def buffer_map_write_async(self, buffer_id: int, start: int, size: int, callback: 'BufferMapWriteCallback', userdata: 'uint8'):
        """
        void wgpu_buffer_map_write_async(WGPUBufferId buffer_id,
                                         WGPUBufferAddress start,
                                         WGPUBufferAddress size,
                                         WGPUBufferMapWriteCallback callback,
                                         uint8_t *userdata);
        """
        xx = []
        return _lib.wgpu_buffer_map_write_async(buffer_id, start, size, callback, userdata)

    def buffer_unmap(self, buffer_id: int):
        """
        void wgpu_buffer_unmap(WGPUBufferId buffer_id);
        """
        xx = []
        return _lib.wgpu_buffer_unmap(buffer_id)

    def command_encoder_begin_compute_pass(self, encoder_id: 'Id_CommandBuffer_Dummy', desc: 'ComputePassDescriptor'):
        """
        WGPUComputePassId wgpu_command_encoder_begin_compute_pass(WGPUCommandEncoderId encoder_id,
                                                                  const WGPUComputePassDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUComputePassDescriptor', xx)
        return _lib.wgpu_command_encoder_begin_compute_pass(encoder_id, desc)

    def command_encoder_begin_render_pass(self, encoder_id: 'Id_CommandBuffer_Dummy', desc: 'RenderPassDescriptor'):
        """
        WGPURenderPassId wgpu_command_encoder_begin_render_pass(WGPUCommandEncoderId encoder_id,
                                                                const WGPURenderPassDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPURenderPassDescriptor', xx)
        return _lib.wgpu_command_encoder_begin_render_pass(encoder_id, desc)

    def command_encoder_copy_buffer_to_buffer(self, command_encoder_id: 'Id_CommandBuffer_Dummy', source: int, source_offset: int, destination: int, destination_offset: int, size: int):
        """
        void wgpu_command_encoder_copy_buffer_to_buffer(WGPUCommandEncoderId command_encoder_id,
                                                        WGPUBufferId source,
                                                        WGPUBufferAddress source_offset,
                                                        WGPUBufferId destination,
                                                        WGPUBufferAddress destination_offset,
                                                        WGPUBufferAddress size);
        """
        xx = []
        return _lib.wgpu_command_encoder_copy_buffer_to_buffer(command_encoder_id, source, source_offset, destination, destination_offset, size)

    def command_encoder_copy_buffer_to_texture(self, command_encoder_id: 'Id_CommandBuffer_Dummy', source: 'BufferCopyView', destination: 'TextureCopyView', copy_size: 'Extent3d'):
        """
        void wgpu_command_encoder_copy_buffer_to_texture(WGPUCommandEncoderId command_encoder_id,
                                                         const WGPUBufferCopyView *source,
                                                         const WGPUTextureCopyView *destination,
                                                         WGPUExtent3d copy_size);
        """
        xx = []
        source = dict_to_struct(source, 'WGPUBufferCopyView', xx)
        destination = dict_to_struct(destination, 'WGPUTextureCopyView', xx)
        copy_size = dict_to_struct(copy_size, 'WGPUExtent3d', xx)
        return _lib.wgpu_command_encoder_copy_buffer_to_texture(command_encoder_id, source, destination, copy_size)

    def command_encoder_copy_texture_to_buffer(self, command_encoder_id: 'Id_CommandBuffer_Dummy', source: 'TextureCopyView', destination: 'BufferCopyView', copy_size: 'Extent3d'):
        """
        void wgpu_command_encoder_copy_texture_to_buffer(WGPUCommandEncoderId command_encoder_id,
                                                         const WGPUTextureCopyView *source,
                                                         const WGPUBufferCopyView *destination,
                                                         WGPUExtent3d copy_size);
        """
        xx = []
        source = dict_to_struct(source, 'WGPUTextureCopyView', xx)
        destination = dict_to_struct(destination, 'WGPUBufferCopyView', xx)
        copy_size = dict_to_struct(copy_size, 'WGPUExtent3d', xx)
        return _lib.wgpu_command_encoder_copy_texture_to_buffer(command_encoder_id, source, destination, copy_size)

    def command_encoder_copy_texture_to_texture(self, command_encoder_id: 'Id_CommandBuffer_Dummy', source: 'TextureCopyView', destination: 'TextureCopyView', copy_size: 'Extent3d'):
        """
        void wgpu_command_encoder_copy_texture_to_texture(WGPUCommandEncoderId command_encoder_id,
                                                          const WGPUTextureCopyView *source,
                                                          const WGPUTextureCopyView *destination,
                                                          WGPUExtent3d copy_size);
        """
        xx = []
        source = dict_to_struct(source, 'WGPUTextureCopyView', xx)
        destination = dict_to_struct(destination, 'WGPUTextureCopyView', xx)
        copy_size = dict_to_struct(copy_size, 'WGPUExtent3d', xx)
        return _lib.wgpu_command_encoder_copy_texture_to_texture(command_encoder_id, source, destination, copy_size)

    def command_encoder_finish(self, encoder_id: 'Id_CommandBuffer_Dummy', desc: 'CommandBufferDescriptor'):
        """
        WGPUCommandBufferId wgpu_command_encoder_finish(WGPUCommandEncoderId encoder_id,
                                                        const WGPUCommandBufferDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUCommandBufferDescriptor', xx)
        return _lib.wgpu_command_encoder_finish(encoder_id, desc)

    def compute_pass_dispatch(self, pass_id: int, x: int, y: int, z: int):
        """
        void wgpu_compute_pass_dispatch(WGPUComputePassId pass_id, uint32_t x, uint32_t y, uint32_t z);
        """
        xx = []
        return _lib.wgpu_compute_pass_dispatch(pass_id, x, y, z)

    def compute_pass_dispatch_indirect(self, pass_id: int, indirect_buffer_id: int, indirect_offset: int):
        """
        void wgpu_compute_pass_dispatch_indirect(WGPUComputePassId pass_id,
                                                 WGPUBufferId indirect_buffer_id,
                                                 WGPUBufferAddress indirect_offset);
        """
        xx = []
        return _lib.wgpu_compute_pass_dispatch_indirect(pass_id, indirect_buffer_id, indirect_offset)

    def compute_pass_end_pass(self, pass_id: int):
        """
        void wgpu_compute_pass_end_pass(WGPUComputePassId pass_id);
        """
        xx = []
        return _lib.wgpu_compute_pass_end_pass(pass_id)

    def compute_pass_insert_debug_marker(self, _pass_id: int, _label: 'RawString'):
        """
        void wgpu_compute_pass_insert_debug_marker(WGPUComputePassId _pass_id, WGPURawString _label);
        """
        xx = []
        return _lib.wgpu_compute_pass_insert_debug_marker(_pass_id, _label)

    def compute_pass_pop_debug_group(self, _pass_id: int):
        """
        void wgpu_compute_pass_pop_debug_group(WGPUComputePassId _pass_id);
        """
        xx = []
        return _lib.wgpu_compute_pass_pop_debug_group(_pass_id)

    def compute_pass_push_debug_group(self, _pass_id: int, _label: 'RawString'):
        """
        void wgpu_compute_pass_push_debug_group(WGPUComputePassId _pass_id, WGPURawString _label);
        """
        xx = []
        return _lib.wgpu_compute_pass_push_debug_group(_pass_id, _label)

    def compute_pass_set_bind_group(self, pass_id: int, index: int, bind_group_id: int, offsets: int, offsets_length: 'uintptr'):
        """
        void wgpu_compute_pass_set_bind_group(WGPUComputePassId pass_id,
                                              uint32_t index,
                                              WGPUBindGroupId bind_group_id,
                                              const WGPUBufferAddress *offsets,
                                              uintptr_t offsets_length);
        """
        xx = []
        return _lib.wgpu_compute_pass_set_bind_group(pass_id, index, bind_group_id, offsets, offsets_length)

    def compute_pass_set_pipeline(self, pass_id: int, pipeline_id: int):
        """
        void wgpu_compute_pass_set_pipeline(WGPUComputePassId pass_id, WGPUComputePipelineId pipeline_id);
        """
        xx = []
        return _lib.wgpu_compute_pass_set_pipeline(pass_id, pipeline_id)

    def create_surface_from_metal_layer(self, layer):
        """
        WGPUSurfaceId wgpu_create_surface_from_metal_layer(void *layer);
        """
        xx = []
        return _lib.wgpu_create_surface_from_metal_layer(layer)

    def create_surface_from_windows_hwnd(self, _hinstance, hwnd):
        """
        WGPUSurfaceId wgpu_create_surface_from_windows_hwnd(void *_hinstance, void *hwnd);
        """
        xx = []
        return _lib.wgpu_create_surface_from_windows_hwnd(_hinstance, hwnd)

    def create_surface_from_xlib(self, display, window: int):
        """
        WGPUSurfaceId wgpu_create_surface_from_xlib(const void **display, uint64_t window);
        """
        xx = []
        return _lib.wgpu_create_surface_from_xlib(display, window)

    def device_create_bind_group(self, device_id: int, desc: 'BindGroupDescriptor'):
        """
        WGPUBindGroupId wgpu_device_create_bind_group(WGPUDeviceId device_id,
                                                      const WGPUBindGroupDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUBindGroupDescriptor', xx)
        return _lib.wgpu_device_create_bind_group(device_id, desc)

    def device_create_bind_group_layout(self, device_id: int, desc: 'BindGroupLayoutDescriptor'):
        """
        WGPUBindGroupLayoutId wgpu_device_create_bind_group_layout(WGPUDeviceId device_id,
                                                                   const WGPUBindGroupLayoutDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUBindGroupLayoutDescriptor', xx)
        return _lib.wgpu_device_create_bind_group_layout(device_id, desc)

    def device_create_buffer(self, device_id: int, desc: 'BufferDescriptor'):
        """
        WGPUBufferId wgpu_device_create_buffer(WGPUDeviceId device_id, const WGPUBufferDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUBufferDescriptor', xx)
        return _lib.wgpu_device_create_buffer(device_id, desc)

    def device_create_buffer_mapped(self, device_id: int, desc: 'BufferDescriptor', mapped_ptr_out: 'uint8'):
        """
        WGPUBufferId wgpu_device_create_buffer_mapped(WGPUDeviceId device_id,
                                                      const WGPUBufferDescriptor *desc,
                                                      uint8_t **mapped_ptr_out);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUBufferDescriptor', xx)
        return _lib.wgpu_device_create_buffer_mapped(device_id, desc, mapped_ptr_out)

    def device_create_command_encoder(self, device_id: int, desc: 'CommandEncoderDescriptor'):
        """
        WGPUCommandEncoderId wgpu_device_create_command_encoder(WGPUDeviceId device_id,
                                                                const WGPUCommandEncoderDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUCommandEncoderDescriptor', xx)
        return _lib.wgpu_device_create_command_encoder(device_id, desc)

    def device_create_compute_pipeline(self, device_id: int, desc: 'ComputePipelineDescriptor'):
        """
        WGPUComputePipelineId wgpu_device_create_compute_pipeline(WGPUDeviceId device_id,
                                                                  const WGPUComputePipelineDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUComputePipelineDescriptor', xx)
        return _lib.wgpu_device_create_compute_pipeline(device_id, desc)

    def device_create_pipeline_layout(self, device_id: int, desc: 'PipelineLayoutDescriptor'):
        """
        WGPUPipelineLayoutId wgpu_device_create_pipeline_layout(WGPUDeviceId device_id,
                                                                const WGPUPipelineLayoutDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUPipelineLayoutDescriptor', xx)
        return _lib.wgpu_device_create_pipeline_layout(device_id, desc)

    def device_create_render_pipeline(self, device_id: int, desc: 'RenderPipelineDescriptor'):
        """
        WGPURenderPipelineId wgpu_device_create_render_pipeline(WGPUDeviceId device_id,
                                                                const WGPURenderPipelineDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPURenderPipelineDescriptor', xx)
        return _lib.wgpu_device_create_render_pipeline(device_id, desc)

    def device_create_sampler(self, device_id: int, desc: 'SamplerDescriptor'):
        """
        WGPUSamplerId wgpu_device_create_sampler(WGPUDeviceId device_id, const WGPUSamplerDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUSamplerDescriptor', xx)
        return _lib.wgpu_device_create_sampler(device_id, desc)

    def device_create_shader_module(self, device_id: int, desc: 'ShaderModuleDescriptor'):
        """
        WGPUShaderModuleId wgpu_device_create_shader_module(WGPUDeviceId device_id,
                                                            const WGPUShaderModuleDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUShaderModuleDescriptor', xx)
        return _lib.wgpu_device_create_shader_module(device_id, desc)

    def device_create_swap_chain(self, device_id: int, surface_id: int, desc: 'SwapChainDescriptor'):
        """
        WGPUSwapChainId wgpu_device_create_swap_chain(WGPUDeviceId device_id,
                                                      WGPUSurfaceId surface_id,
                                                      const WGPUSwapChainDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUSwapChainDescriptor', xx)
        return _lib.wgpu_device_create_swap_chain(device_id, surface_id, desc)

    def device_create_texture(self, device_id: int, desc: 'TextureDescriptor'):
        """
        WGPUTextureId wgpu_device_create_texture(WGPUDeviceId device_id, const WGPUTextureDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUTextureDescriptor', xx)
        return _lib.wgpu_device_create_texture(device_id, desc)

    def device_destroy(self, device_id: int):
        """
        void wgpu_device_destroy(WGPUDeviceId device_id);
        """
        xx = []
        return _lib.wgpu_device_destroy(device_id)

    def device_get_limits(self, _device_id: int, limits: 'Limits'):
        """
        void wgpu_device_get_limits(WGPUDeviceId _device_id, WGPULimits *limits);
        """
        xx = []
        limits = dict_to_struct(limits, 'WGPULimits', xx)
        return _lib.wgpu_device_get_limits(_device_id, limits)

    def device_get_queue(self, device_id: int):
        """
        WGPUQueueId wgpu_device_get_queue(WGPUDeviceId device_id);
        """
        xx = []
        return _lib.wgpu_device_get_queue(device_id)

    def device_poll(self, device_id: int, force_wait: 'bool'):
        """
        void wgpu_device_poll(WGPUDeviceId device_id, bool force_wait);
        """
        xx = []
        return _lib.wgpu_device_poll(device_id, force_wait)

    def queue_submit(self, queue_id: 'Id_Device_Dummy', command_buffers: int, command_buffers_length: 'uintptr'):
        """
        void wgpu_queue_submit(WGPUQueueId queue_id,
                               const WGPUCommandBufferId *command_buffers,
                               uintptr_t command_buffers_length);
        """
        xx = []
        return _lib.wgpu_queue_submit(queue_id, command_buffers, command_buffers_length)

    def render_pass_draw(self, pass_id: int, vertex_count: int, instance_count: int, first_vertex: int, first_instance: int):
        """
        void wgpu_render_pass_draw(WGPURenderPassId pass_id,
                                   uint32_t vertex_count,
                                   uint32_t instance_count,
                                   uint32_t first_vertex,
                                   uint32_t first_instance);
        """
        xx = []
        return _lib.wgpu_render_pass_draw(pass_id, vertex_count, instance_count, first_vertex, first_instance)

    def render_pass_draw_indexed(self, pass_id: int, index_count: int, instance_count: int, first_index: int, base_vertex: int, first_instance: int):
        """
        void wgpu_render_pass_draw_indexed(WGPURenderPassId pass_id,
                                           uint32_t index_count,
                                           uint32_t instance_count,
                                           uint32_t first_index,
                                           int32_t base_vertex,
                                           uint32_t first_instance);
        """
        xx = []
        return _lib.wgpu_render_pass_draw_indexed(pass_id, index_count, instance_count, first_index, base_vertex, first_instance)

    def render_pass_draw_indexed_indirect(self, pass_id: int, indirect_buffer_id: int, indirect_offset: int):
        """
        void wgpu_render_pass_draw_indexed_indirect(WGPURenderPassId pass_id,
                                                    WGPUBufferId indirect_buffer_id,
                                                    WGPUBufferAddress indirect_offset);
        """
        xx = []
        return _lib.wgpu_render_pass_draw_indexed_indirect(pass_id, indirect_buffer_id, indirect_offset)

    def render_pass_draw_indirect(self, pass_id: int, indirect_buffer_id: int, indirect_offset: int):
        """
        void wgpu_render_pass_draw_indirect(WGPURenderPassId pass_id,
                                            WGPUBufferId indirect_buffer_id,
                                            WGPUBufferAddress indirect_offset);
        """
        xx = []
        return _lib.wgpu_render_pass_draw_indirect(pass_id, indirect_buffer_id, indirect_offset)

    def render_pass_end_pass(self, pass_id: int):
        """
        void wgpu_render_pass_end_pass(WGPURenderPassId pass_id);
        """
        xx = []
        return _lib.wgpu_render_pass_end_pass(pass_id)

    def render_pass_execute_bundles(self, _pass_id: int, _bundles: int, _bundles_length: 'uintptr'):
        """
        void wgpu_render_pass_execute_bundles(WGPURenderPassId _pass_id,
                                              const WGPURenderBundleId *_bundles,
                                              uintptr_t _bundles_length);
        """
        xx = []
        return _lib.wgpu_render_pass_execute_bundles(_pass_id, _bundles, _bundles_length)

    def render_pass_insert_debug_marker(self, _pass_id: int, _label: 'RawString'):
        """
        void wgpu_render_pass_insert_debug_marker(WGPURenderPassId _pass_id, WGPURawString _label);
        """
        xx = []
        return _lib.wgpu_render_pass_insert_debug_marker(_pass_id, _label)

    def render_pass_pop_debug_group(self, _pass_id: int):
        """
        void wgpu_render_pass_pop_debug_group(WGPURenderPassId _pass_id);
        """
        xx = []
        return _lib.wgpu_render_pass_pop_debug_group(_pass_id)

    def render_pass_push_debug_group(self, _pass_id: int, _label: 'RawString'):
        """
        void wgpu_render_pass_push_debug_group(WGPURenderPassId _pass_id, WGPURawString _label);
        """
        xx = []
        return _lib.wgpu_render_pass_push_debug_group(_pass_id, _label)

    def render_pass_set_bind_group(self, pass_id: int, index: int, bind_group_id: int, offsets: int, offsets_length: 'uintptr'):
        """
        void wgpu_render_pass_set_bind_group(WGPURenderPassId pass_id,
                                             uint32_t index,
                                             WGPUBindGroupId bind_group_id,
                                             const WGPUBufferAddress *offsets,
                                             uintptr_t offsets_length);
        """
        xx = []
        return _lib.wgpu_render_pass_set_bind_group(pass_id, index, bind_group_id, offsets, offsets_length)

    def render_pass_set_blend_color(self, pass_id: int, color: 'Color'):
        """
        void wgpu_render_pass_set_blend_color(WGPURenderPassId pass_id, const WGPUColor *color);
        """
        xx = []
        color = dict_to_struct(color, 'WGPUColor', xx)
        return _lib.wgpu_render_pass_set_blend_color(pass_id, color)

    def render_pass_set_index_buffer(self, pass_id: int, buffer_id: int, offset: int):
        """
        void wgpu_render_pass_set_index_buffer(WGPURenderPassId pass_id,
                                               WGPUBufferId buffer_id,
                                               WGPUBufferAddress offset);
        """
        xx = []
        return _lib.wgpu_render_pass_set_index_buffer(pass_id, buffer_id, offset)

    def render_pass_set_pipeline(self, pass_id: int, pipeline_id: int):
        """
        void wgpu_render_pass_set_pipeline(WGPURenderPassId pass_id, WGPURenderPipelineId pipeline_id);
        """
        xx = []
        return _lib.wgpu_render_pass_set_pipeline(pass_id, pipeline_id)

    def render_pass_set_scissor_rect(self, pass_id: int, x: int, y: int, w: int, h: int):
        """
        void wgpu_render_pass_set_scissor_rect(WGPURenderPassId pass_id,
                                               uint32_t x,
                                               uint32_t y,
                                               uint32_t w,
                                               uint32_t h);
        """
        xx = []
        return _lib.wgpu_render_pass_set_scissor_rect(pass_id, x, y, w, h)

    def render_pass_set_stencil_reference(self, pass_id: int, value: int):
        """
        void wgpu_render_pass_set_stencil_reference(WGPURenderPassId pass_id, uint32_t value);
        """
        xx = []
        return _lib.wgpu_render_pass_set_stencil_reference(pass_id, value)

    def render_pass_set_vertex_buffers(self, pass_id: int, start_slot: int, buffers: int, offsets: int, length: 'uintptr'):
        """
        void wgpu_render_pass_set_vertex_buffers(WGPURenderPassId pass_id,
                                                 uint32_t start_slot,
                                                 const WGPUBufferId *buffers,
                                                 const WGPUBufferAddress *offsets,
                                                 uintptr_t length);
        """
        xx = []
        return _lib.wgpu_render_pass_set_vertex_buffers(pass_id, start_slot, buffers, offsets, length)

    def render_pass_set_viewport(self, pass_id: int, x: float, y: float, w: float, h: float, min_depth: float, max_depth: float):
        """
        void wgpu_render_pass_set_viewport(WGPURenderPassId pass_id,
                                           float x,
                                           float y,
                                           float w,
                                           float h,
                                           float min_depth,
                                           float max_depth);
        """
        xx = []
        return _lib.wgpu_render_pass_set_viewport(pass_id, x, y, w, h, min_depth, max_depth)

    def request_adapter_async(self, desc: 'RequestAdapterOptions', mask: int, callback: 'RequestAdapterCallback', userdata):
        """
        void wgpu_request_adapter_async(const WGPURequestAdapterOptions *desc,
                                        WGPUBackendBit mask,
                                        WGPURequestAdapterCallback callback,
                                        void *userdata);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPURequestAdapterOptions', xx)
        return _lib.wgpu_request_adapter_async(desc, mask, callback, userdata)

    def sampler_destroy(self, sampler_id: int):
        """
        void wgpu_sampler_destroy(WGPUSamplerId sampler_id);
        """
        xx = []
        return _lib.wgpu_sampler_destroy(sampler_id)

    def swap_chain_get_next_texture(self, swap_chain_id: int):
        """
        WGPUSwapChainOutput wgpu_swap_chain_get_next_texture(WGPUSwapChainId swap_chain_id);
        """
        xx = []
        return _lib.wgpu_swap_chain_get_next_texture(swap_chain_id)

    def swap_chain_present(self, swap_chain_id: int):
        """
        void wgpu_swap_chain_present(WGPUSwapChainId swap_chain_id);
        """
        xx = []
        return _lib.wgpu_swap_chain_present(swap_chain_id)

    def texture_create_view(self, texture_id: int, desc: 'TextureViewDescriptor'):
        """
        WGPUTextureViewId wgpu_texture_create_view(WGPUTextureId texture_id,
                                                   const WGPUTextureViewDescriptor *desc);
        """
        xx = []
        desc = dict_to_struct(desc, 'WGPUTextureViewDescriptor', xx)
        return _lib.wgpu_texture_create_view(texture_id, desc)

    def texture_destroy(self, texture_id: int):
        """
        void wgpu_texture_destroy(WGPUTextureId texture_id);
        """
        xx = []
        return _lib.wgpu_texture_destroy(texture_id)

    def texture_view_destroy(self, texture_view_id: int):
        """
        void wgpu_texture_view_destroy(WGPUTextureViewId texture_view_id);
        """
        xx = []
        return _lib.wgpu_texture_view_destroy(texture_view_id)
