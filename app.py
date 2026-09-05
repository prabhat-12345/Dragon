import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neon Dragon Run", layout="centered")
st.title("🐉 Automatic Running Neon Dragon")
st.caption("Dragon apne aap chamakti makkhi (Red Target) ke peeche daud raha hai!")

html_code = """
<div style="background-color: #0b0b0b; display: flex; justify-content: center; align-items: center; height: 75vh; width: 100%; overflow: hidden; position: relative; border-radius: 12px;">
    <canvas id="dragonCanvas" style="display: block; width: 100%; height: 100%;"></canvas>
</div>
<script>
    const canvas = document.getElementById('dragonCanvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;

    // Automatic Target (Makkhi) jo screen par bhagegi
    const target = {
        x: canvas.width / 2,
        y: canvas.height / 2,
        targetX: Math.random() * canvas.width,
        targetY: Math.random() * canvas.height,
        speed: 3 // Makkhi ki speed
    };

    // Dragon ka starting position
    const dragonHead = { x: canvas.width / 4, y: canvas.height / 2 };

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
        drawBone(color) {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.angle);
            
            ctx.strokeStyle = color;
            ctx.lineWidth = 2.5;
            ctx.shadowBlur = 10;
            ctx.shadowColor = color;
            
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
    const numSegments = 35; 
    const segmentLength = 13; 

    for (let i = 0; i < numSegments; i++) {
        let size = Math.sin((i / numSegments) * Math.PI) * 18;
        if(i < 4) size = 8 + i * 2; 
        segments.push(new Segment(dragonHead.x, dragonHead.y, segmentLength, size));
    }

    function drawLeg(startX, startY, angle, side, phase, color) {
        ctx.save();
        ctx.translate(startX, startY);
        ctx.rotate(angle + (side * Math.PI / 2.5) + Math.sin(phase) * 0.3);
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5;
        ctx.shadowBlur = 8;
        ctx.shadowColor = color;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(20, 0);
        ctx.lineTo(28, 10 * side);
        ctx.stroke();
        ctx.restore();
    }

    let animationFrame = 0;

    function loop() {
        ctx.fillStyle = 'rgba(11, 11, 11, 0.22)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        animationFrame++;

        // 1. Makkhi (Target) ko random chalane ka logic
        let tDx = target.targetX - target.x;
        let tDy = target.targetY - target.y;
        let tDist = Math.sqrt(tDx * tDx + tDy * tDy);

        if (tDist < 20) {
            // Agar makkhi ek kone par pahunch jaye, toh naya random kona chunon
            target.targetX = Math.random() * (canvas.width - 40) + 20;
            target.targetY = Math.random() * (canvas.height - 40) + 20;
        } else {
            // Makkhi ko agle point ki taraf smoothly badhana
            target.x += (tDx / tDist) * target.speed;
            target.y += (tDy / tDist) * target.speed;
        }

        // Chamakti hui laal makkhi draw karna
        ctx.save();
        ctx.fillStyle = "#ff0055";
        ctx.shadowBlur = 15;
        ctx.shadowColor = "#ff0055";
        ctx.beginPath();
        ctx.arc(target.x, target.y, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // 2. Dragon ka Sar (Head) makkhi ke peeche smoothly bhagane ka logic
        let dDx = target.x - dragonHead.x;
        let dDy = target.y - dragonHead.y;
        let dDist = Math.sqrt(dDx * dDx + dDy * dDy);
        
        // Dragon ki daudne ki speed (Makkhi se thodi kam rakhi h tak ki chase lamba chale)
        let dragonSpeed = 2.6; 
        if (dDist > 5) {
            dragonHead.x += (dDx / dDist) * dragonSpeed;
            dragonHead.y += (dDy / dDist) * dragonSpeed;
        }

        let targetX = dragonHead.x;
        let targetY = dragonHead.y;
        const dragonColor = "#00ff99";

        // Head Drawing with Glowing Eyes
        ctx.save();
        let headAngle = segments.length > 0 ? segments[0].angle : 0;
        ctx.translate(targetX, targetY);
        ctx.rotate(headAngle);
        
        ctx.fillStyle = "#ffffff";
        ctx.shadowBlur = 15;
        ctx.shadowColor = dragonColor;
        ctx.beginPath();
        ctx.arc(0, 0, 7, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = "#ff0055";
        ctx.shadowColor = "#ff0055";
        ctx.beginPath();
        ctx.arc(2, -3, 1.8, 0, Math.PI * 2);
        ctx.arc(2, 3, 1.8, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Saari body segments ko update aur draw karna
        for (let i = 0; i < segments.length; i++) {
            segments[i].update(targetX, targetY);
            segments[i].drawBone(dragonColor);
            
            if (i == 5) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.2, dragonColor);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.2, dragonColor);
            }
            if (i == 15) { 
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, 1, animationFrame * 0.2 + Math.PI, dragonColor);
                drawLeg(segments[i].x, segments[i].y, segments[i].angle, -1, animationFrame * 0.2 + Math.PI, dragonColor);
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
