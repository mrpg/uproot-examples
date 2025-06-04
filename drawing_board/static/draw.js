const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let isDrawing = false;
let currentStroke = [];
let points = [];
let allStrokes = [];
const minDistance = 3;

function resizeCanvas() {
    canvas.width = 800;
    canvas.height = 400;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.lineWidth = 2;
    ctx.strokeStyle = uproot.vars.color;
    redrawAll();
}

function getEventPos(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.clientX || (e.touches && e.touches[0].clientX);
    const clientY = e.clientY || (e.touches && e.touches[0].clientY);
    return {
        x: clientX - rect.left,
        y: clientY - rect.top,
    };
}

function getDistance(p1, p2) {
    return Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
}

function drawSmoothStroke(points) {
    if (points.length < 2) return;

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 1; i < points.length - 2; i++) {
        const xc = (points[i].x + points[i + 1].x) / 2;
        const yc = (points[i].y + points[i + 1].y) / 2;
        ctx.quadraticCurveTo(points[i].x, points[i].y, xc, yc);
    }

    if (points.length > 1) {
        const last = points[points.length - 1];
        const secondLast = points[points.length - 2];
        ctx.quadraticCurveTo(secondLast.x, secondLast.y, last.x, last.y);
    }

    ctx.stroke();
}

function redrawAll() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    allStrokes.forEach(stroke => {
        ctx.strokeStyle = stroke.color;
        ctx.lineWidth = stroke.lineWidth;
        drawSmoothStroke(stroke.points);
    });
    ctx.strokeStyle = uproot.vars.color;
    ctx.lineWidth = 2;
}

function startDrawing(e) {
    e.preventDefault();
    isDrawing = true;
    const pos = getEventPos(e);
    points = [pos];
    currentStroke = [pos];
}

function draw(e) {
    if (!isDrawing) return;
    e.preventDefault();

    const pos = getEventPos(e);

    if (points.length === 0 || getDistance(pos, points[points.length - 1]) >= minDistance) {
        const prevPoint = points[points.length - 1];
        points.push(pos);
        currentStroke.push(pos);

        if (prevPoint) {
            ctx.beginPath();
            ctx.moveTo(prevPoint.x, prevPoint.y);
            ctx.lineTo(pos.x, pos.y);
            ctx.stroke();
        }
    }
}

function stopDrawing(e) {
    if (!isDrawing) return;
    e.preventDefault();
    isDrawing = false;

    if (currentStroke.length > 1) {
        const strokeData = {
            points: [...points],
            color: uproot.vars.color,
            lineWidth: ctx.lineWidth
        };
        allStrokes.push(strokeData);
        sendStrokeToServer(currentStroke);
    }

    points = [];
    currentStroke = [];
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    allStrokes = [];
}

function sendStrokeToServer(stroke) {
    const strokeData = {
        points: stroke,
        lineWidth: ctx.lineWidth,
    };

    uproot.invoke("stroke", strokeData);
}

function drawReceivedStrokes(strokeDataArray) {
    strokeDataArray.forEach(strokeData => {
        allStrokes.push(strokeData);
    });
    redrawAll();
}

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseout", stopDrawing);

canvas.addEventListener("touchstart", startDrawing);
canvas.addEventListener("touchmove", draw);
canvas.addEventListener("touchend", stopDrawing);
canvas.addEventListener("touchcancel", stopDrawing);

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
