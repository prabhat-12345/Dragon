import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Dragon Cursor", layout="centered")
st.title("🐉 Mobile Interactive Dragon")
st.caption("Screen par ungli (touch) ghumao, dragon peeche chalega!")

html_code = """
<div style="background-color: #111; display: flex; justify-content: center; align-items: center; height: 75vh; width: 100%; overflow: hidden; position: relative;">
    <canvas id="dragonCanvas" style="display: block; width: 100%; height: 100%;"></canvas>
</div>
<script>
    const canvas = document.getElementById('dragonCanvas');
    const ctx = canvas.getContext('2d');
    
    // Mobile screen ke hisaab se auto size
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;

    const mouse = { x: canvas.width / 2, y: canvas.height / 2 };

    // Mobile Touch Support (Ungli ghumane par track karega)
    canvas.addEventListener('touchmove', (e) => {
        if(e.touches.length > 0) {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.touches[0].clientX - rect.left;
            mouse.y = e.touches[0].clientY - rect.top;
            e.preventDefault(); // Page up-down hone se rokne ke liye
        }
    }, { passive: false });

    // Laptop/PC ke liye mouse check
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });

    class Segment {
        constructor(x, y, length, size) {
            this.x = x;
            this.y = y;
            this.length = length;
            this.size = size;
            this.angle = 0;
        }
        update(targetX, targetY) {
            let dx = targetX - this.x;
            let dy = targetY - this.y;
            this.angle = Math.atan2(dy, dx);
            this.x = targetX - Math.cos(this.angle) * this.length;
            this.y = targetY - Math.sin(this.angle) * this.length;
        }
        drawBone() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);
            ctx.strokeStyle = "rgba(240, 240, 240, 0.85)";
            ctx.lineWidth = 2;
            if (this.size > 2) {
                ctx.beginPath();
                ctx.moveTo(0, -this.size);
                ctx.quadraticCurveTo(this.length / 2, -this.size * 0.8, this.length, 0);
                ctx.quadraticCurveTo(this.length / 2, this.size * 0.8, 0, this.size);
                ctx.stroke();
            } else {
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(this.length, 0);
                ctx.stroke();
            }
            ctx.restore();
        }
    }

    const segments = [];
    const numSegments = 30; // Mobile par lag na ho isliye thoda compact kiya
    const segmentLength = 12; 

    for (let i = 0; i < numSegments; i++) {
        let size = Math.sin((i / numSegments) * Math.PI) * 16;
        if(i < 4) size = 8 + i * 2; 
        segments.push(new Segment(mouse.x, mouse.y, segmentLength, size));
    }

    function drawLeg(startX, startY, angle, side, phase) {
        ctx.save();
        ctx.translate(startX, startY);
        ctx.rotate(angle + (side * Math.PI / 2.5) + Math.sin(phase) * 0.25);
        ctx.strokeStyle = "rgba(210, 210, 210, 0.9)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(18, 0);
        ctx.lineTo(26, 10 * side);
        ctx.stroke();
        ctx.restore();
    }

    let animationFrame = 0;
    function loop() {
        ctx.fillStyle = 'rgba(17, 17, 17, 0.25)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        animationFrame++;

        let targetX = mouse.x;
        let targetY = mouse.y;

        for (let i = 0; i < segments.length; i++) {
            segments[i].update(targetX, targetY);
            segments[i].drawBone();
            if (i == 5) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.15);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.15);
            }
            if (i == 14) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.15 + Math.PI);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.15 + Math.PI);
            }
            targetX = segments[i].x;
            targetY = segments[i].y;
        }
        requestAnimationFrame(loop);
    }
    loop();
</script>
"""
components.html(html_code, height=500, scrolling=False)
