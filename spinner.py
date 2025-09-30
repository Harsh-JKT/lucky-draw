import streamlit.components.v1 as components
import random
import json

import streamlit.components.v1 as components
import random
import json

import streamlit.components.v1 as components
import math
import json

def spin_wheel_image_org(
    names,
    winner,
    duration_sec=2.8,
    key="wheel",
    wheel_url="wheel.png",
    num_slices=None,            # defaults to len(names) if not provided
    clockwise=True,             # are your labels/slices arranged clockwise?
    start_angle_deg=0.0,        # where is slice index 0's CENTER vs the pointer? (degrees)
    pointer_at="top",           # "top" | "right" | "bottom" | "left"
    extra_spins=5,              # whole turns for drama
    size_px=380                 # wheel size
):
    """
    Spin a static wheel image and stop on `winner`.

    Geometry:
    - The pointer is fixed; by default it's at the top (12 o'clock).
    - 0° is at the pointer direction. Angles increase clockwise if `clockwise=True`.
    - `start_angle_deg` says where the CENTER of slice index 0 sits initially, relative to the pointer.
      Example: if your art's slice 0 center is already at the top, use 0.
               if it’s centered at the RIGHT, use +90; at the BOTTOM, +180; at the LEFT, +270.
    """
    N = num_slices or len(names)
    if N <= 0:
        raise ValueError("Need at least 1 slice")

    # Which slice index is our winner?
    try:
        target_idx = names.index(winner)
    except ValueError:
        target_idx = 0  # fallback

    # Pointer direction offset
    pointer_map = {"top": 0.0, "right": 90.0, "bottom": 180.0, "left": 270.0}
    pointer_deg = pointer_map.get(pointer_at, 0.0)

    # Angle per slice
    slice_deg = 360.0 / N

    # Where is the target slice's CENTER initially (relative to pointer)?
    # If clockwise: centers go +slice_deg each step; else minus.
    direction = 1.0 if clockwise else -1.0
    target_center_deg = start_angle_deg + direction * (target_idx + 0.5) * slice_deg

    # We want to rotate the WHEEL so that target_center ends up at the pointer direction.
    # Positive CSS rotate() is clockwise. To move content so its center comes to pointer:
    # final_rotation = extra_spins*360 + (pointer_deg - target_center_deg)
    final_rotation = extra_spins * 360.0 + (pointer_deg - target_center_deg)

    payload = {
        "duration": duration_sec,
        "finalRotation": final_rotation,
        "wheelUrl": wheel_url,
        "size": size_px
    }

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; gap:12px;">
      <div style="position:relative; width:{size_px}px; height:{size_px}px;">
        <!-- Pointer (stays fixed) -->
        <div style="
          position:absolute; left:50%; transform:translateX(-50%);
          {'top:-12px;' if pointer_at=='top' else ''}
          {'bottom:-12px;' if pointer_at=='bottom' else ''}
          {'left:auto; top:50%; transform:translateY(-50%); right:-12px;' if pointer_at=='right' else ''}
          {'left:-12px; top:50%; transform:translateY(-50%);' if pointer_at=='left' else ''}
          width:0; height:0; 
          {'border-left:15px solid transparent; border-right:15px solid transparent; border-bottom:30px solid gold;' if pointer_at=='top' else ''}
          {'border-left:15px solid transparent; border-right:15px solid transparent; border-top:30px solid gold;' if pointer_at=='bottom' else ''}
          {'border-top:15px solid transparent; border-bottom:15px solid transparent; border-left:30px solid gold;' if pointer_at=='right' else ''}
          {'border-top:15px solid transparent; border-bottom:15px solid transparent; border-right:30px solid gold;' if pointer_at=='left' else ''}
          z-index:5; filter: drop-shadow(0 2px 2px rgba(0,0,0,.35));
        "></div>

        <!-- Wheel image (perfectly centered, square, masked as circle) -->
        <img id="wheel-{key}" src="{payload['wheelUrl']}"
             style="
               width:100%; height:100%;
               object-fit: contain;              /* no stretch */
               display:block;
               border-radius:50%;                /* circular mask */
               border:8px solid gold;
               box-shadow:0 10px 40px rgba(0,0,0,.4), inset 0 0 18px rgba(255,255,255,.25);
               transform-origin:50% 50%;         /* rotate around center */
             " />
      </div>
      <div id="status-{key}" style="color:white; font-weight:600;">Spinning…</div>
    </div>

    <script>
      (function() {{
        const img = document.getElementById("wheel-{key}");
        img.style.transition = "transform {payload['duration']}s cubic-bezier(.12,.65,.13,1)";
        requestAnimationFrame(() => {{
          img.style.transform = "rotate({payload['finalRotation']}deg)";
        }});
        setTimeout(() => {{
          document.getElementById("status-{key}").innerText = "Stopped!";
        }}, {int(payload['duration']*1000)});
      }})();
    </script>
    """
    components.html(html, height=size_px + 80)


# def spin_wheel_image_org(names, winner, duration_sec=3.0, key="wheel", wheel_url="wheel.png"):
#     N = len(names)
#     seg_angle = 360 / N
#     target_idx = names.index(winner)
#     target_angle = (target_idx + 0.5) * seg_angle  # center of slice
    
#     # Rotate multiple spins + align winner to top
#     extra_spins = 5
#     final_rotation = extra_spins * 360 + (360 - target_angle)

#     payload = {
#         "duration": duration_sec,
#         "finalRotation": final_rotation,
#         "wheelUrl": wheel_url
#     }

#     html = f"""
#     <div style="display:flex; flex-direction:column; align-items:center; gap:12px;">
#       <div style="position:relative; width:380px; height:380px;">
#         <!-- Pointer -->
#         <div style="
#           position:absolute; top:-12px; left:50%; transform:translateX(-50%);
#           width:0; height:0; border-left:15px solid transparent; border-right:15px solid transparent;
#           border-bottom:30px solid gold; z-index:5;
#         "></div>

#         <!-- Wheel Image -->
#         <img id="wheel-{key}" src="{payload['wheelUrl']}" 
#              style="width:100%; height:100%; border-radius:50%; border:6px solid gold; box-shadow:0 10px 40px rgba(0,0,0,.4);" />
#       </div>
#       <div id="status-{key}" style="color:white; font-weight:600;">Spinning…</div>
#     </div>

#     <script>
#       const img = document.getElementById("wheel-{key}");
#       img.style.transition = "transform {payload['duration']}s cubic-bezier(.12,.65,.13,1)";
#       requestAnimationFrame(() => {{
#         img.style.transform = "rotate({payload['finalRotation']}deg)";
#       }});
#       setTimeout(() => {{
#         document.getElementById("status-{key}").innerText = "Stopped!";
#       }}, {int(duration_sec*1000)});
#     </script>
#     """
#     components.html(html, height=460)


def spin_wheel_image(names, winner, duration_sec=3.0, key="wheel", wheel_url="wheel.png"):
    N = len(names)
    seg_angle = 360 / N
    target_idx = names.index(winner)
    target_angle = (target_idx + 0.5) * seg_angle  # center of slice
    
    # Rotate multiple spins + align winner to top
    extra_spins = 5
    final_rotation = extra_spins * 360 + (360 - target_angle)

    payload = {
        "duration": duration_sec,
        "finalRotation": final_rotation,
        "wheelUrl": wheel_url
    }

    html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; gap:12px;">
      <div style="position:relative; width:380px; height:380px;">
        <!-- Pointer -->
        <div style="
          position:absolute; top:-12px; left:50%; transform:translateX(-50%);
          width:0; height:0; border-left:15px solid transparent; border-right:15px solid transparent;
          border-bottom:30px solid gold; z-index:5;
        "></div>

        <!-- Wheel Image -->
        <img id="wheel-{key}" src="{payload['wheelUrl']}" 
             style="width:100%; height:100%; border-radius:50%; border:6px solid gold; box-shadow:0 10px 40px rgba(0,0,0,.4);" />
      </div>
      <div id="status-{key}" style="color:white; font-weight:600;">Spinning…</div>
    </div>

    <script>
      const img = document.getElementById("wheel-{key}");
      img.style.transition = "transform {payload['duration']}s cubic-bezier(.12,.65,.13,1)";
      requestAnimationFrame(() => {{
        img.style.transform = "rotate({payload['finalRotation']}deg)";
      }});
      setTimeout(() => {{
        document.getElementById("status-{key}").innerText = "Stopped!";
      }}, {int(duration_sec*1000)});
    </script>
    """
    components.html(html, height=460)
