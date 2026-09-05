import streamlit as st
import streamlit.components.v1 as components

# Page Layout Configuration
st.set_page_config(page_title="Interactive Dragon Cursor", layout="centered")
st.title("🐉 Interactive Skeletal Dragon Web App")
st.caption("Apne mouse/cursor ko screen par ghumao aur dragon aapko follow karega!")

# HTML + CSS + JS Integration for Canvas Animation
html_code = """
<div style="background-color: #111; display: flex; justify-content: center; align-items: center; height: 80vh; width: 100%; overflow: hidden; position: relative;">
    <canvas id="dragonCanvas" style="display: block; cursor: crosshair;"></canvas>
</div>
<script>
    const canvas = document.getElementById('dragonCanvas');
    const ctx = canvas.getContext('2d');
    
    // Canvas dimensions within container
    canvas.width = 700;
    canvas.height = 550;
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    const mouse = { x: centerX, y: centerY };

    // Container ke andar mouse track karne ke liye event listener
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });

    // Touch screen mobiles ke liye support
    canvas.addEventListener('touchmove', (e) => {
        if(e.touches.length > 0) {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.touches[0].clientX - rect.left;
            mouse.y = e.touches[0].clientY - rect.top;
            e.preventDefault();
        }
    }, { passive: False });

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
            
            // Spine Point
            ctx.beginPath();
            ctx.arc(0, 0, 1.5, 0, Math.PI * 2);
            ctx.fillStyle = "#fff";
            ctx.fill();

            // Ribs Drawing
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
    const numSegments = 38; 
    const segmentLength = 13; 

    for (let i = 0; i < numSegments; i++) {
        let size = Math.sin((i / numSegments) * Math.PI) * 20;
        if(i < 5) size = 10 + i * 2; 
        segments.push(new Segment(mouse.x, mouse.y, segmentLength, size));
    }

    function drawLeg(startX, startY, angle, side, phase) {
        ctx.save();
        ctx.translate(startX, startY);
        ctx.rotate(angle + (side * Math.PI / 2.5) + Math.sin(phase) * 0.25);
        
        ctx.strokeStyle = "rgba(210, 210, 210, 0.9)";
        ctx.lineWidth = 2.5;
        
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(22, 0);
        ctx.lineTo(32, 12 * side);
        ctx.stroke();
        ctx.restore();
    }

    let animationFrame = 0;

    function loop() {
        // Trail Motion effect paida karne ke liye semi-transparent overlay
        ctx.fillStyle = 'rgba(17, 17, 17, 0.25)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        animationFrame++;

        let targetX = mouse.x;
        let targetY = mouse.y;

        // Head Drawing Logic
        ctx.save();
        let headAngle = segments[0] ? segments[0].angle : 0;
        ctx.translate(targetX, targetY);
        ctx.rotate(headAngle);
        ctx.fillStyle = "#fff";
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        ctx.arc(0, 0, 6, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.beginPath();
        ctx.moveTo(4, -3); ctx.lineTo(-10, -8);
        ctx.moveTo(4, 3); ctx.lineTo(-10, 8);
        ctx.stroke();
        ctx.restore();

        // Segments Chain loop
        for (let i = 0; i < segments.length; i++) {
            segments[i].update(targetX, targetY);
            segments[i].drawBone();
            
            if (i === 6) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.12);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.12);
            }
            if (i === 16) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.12 + Math.PI);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.12 + Math.PI);
            }

            targetX = segments[i].x;
            targetY = segments[i].y;
        }

        requestAnimationFrame(loop);
    }

    // Direct loop call
    loop();
</script>
"""

# Streamlit application mein html content render karein
components.html(html_code, height=600, scrolling=False)
