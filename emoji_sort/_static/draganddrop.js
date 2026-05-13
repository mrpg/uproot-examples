(function () {
    "use strict";

    // — DOM references —
    const source  = document.getElementById("source");
    const bucket1 = document.getElementById("bucket1");
    const bucket2 = document.getElementById("bucket2");
    const count1  = document.getElementById("count1");
    const count2  = document.getElementById("count2");

    // All drop zones (source area + both buckets).
    const dropZones = [source, bucket1, bucket2];

    // — Helpers —

    /**
     * For a given item element, find the matching hidden radio input and
     * set its value based on which bucket the item is currently in.
     */
    function syncField(item) {
        var idx    = item.dataset.index;
        var name   = "item_" + idx;
        var radios = document.querySelectorAll('input[name="' + name + '"]');

        var parent = item.parentElement;
        var value  = null;
        if (parent === bucket1) value = "1";
        if (parent === bucket2) value = "2";

        radios.forEach(function (r) {
            r.checked = (r.value === value);
        });
    }

    /** Update badge counters. */
    function syncAll() {
        count1.textContent = bucket1.querySelectorAll(".draggable-item").length;
        count2.textContent = bucket2.querySelectorAll(".draggable-item").length;
    }

    // — Drag events —

    document.addEventListener("dragstart", function (e) {
        var item = e.target.closest(".draggable-item");
        if (!item) return;
        e.dataTransfer.setData("text/plain", item.id);
        e.dataTransfer.effectAllowed = "move";
        requestAnimationFrame(function () { item.classList.add("opacity-50"); });
    });

    document.addEventListener("dragend", function (e) {
        var item = e.target.closest(".draggable-item");
        if (item) item.classList.remove("opacity-50");
    });

    // — Drop zone events —

    dropZones.forEach(function (zone) {
        zone.addEventListener("dragover", function (e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = "move";
            zone.classList.add("border-primary");
        });

        zone.addEventListener("dragleave", function (e) {
            if (!zone.contains(e.relatedTarget)) {
                zone.classList.remove("border-primary");
            }
        });

        zone.addEventListener("drop", function (e) {
            e.preventDefault();
            zone.classList.remove("border-primary");

            var id   = e.dataTransfer.getData("text/plain");
            var item = document.getElementById(id);
            if (!item) return;

            zone.appendChild(item);
            syncField(item);
            syncAll();
        });
    });

    // — Touch support —

    var touchItem   = null;
    var touchClone  = null;
    var touchStartX = 0;
    var touchStartY = 0;

    document.addEventListener("touchstart", function (e) {
        var item = e.target.closest(".draggable-item");
        if (!item) return;

        touchItem   = item;
        var rect    = item.getBoundingClientRect();
        touchStartX = e.touches[0].clientX - rect.left;
        touchStartY = e.touches[0].clientY - rect.top;

        touchClone = item.cloneNode(true);
        touchClone.style.position = "fixed";
        touchClone.style.zIndex   = "9999";
        touchClone.style.pointerEvents = "none";
        touchClone.style.opacity  = "0.8";
        touchClone.style.width    = rect.width + "px";
        document.body.appendChild(touchClone);

        item.classList.add("opacity-25");
    }, { passive: true });

    document.addEventListener("touchmove", function (e) {
        if (!touchClone) return;
        e.preventDefault();
        touchClone.style.left = (e.touches[0].clientX - touchStartX) + "px";
        touchClone.style.top  = (e.touches[0].clientY - touchStartY) + "px";
    }, { passive: false });

    document.addEventListener("touchend", function (e) {
        if (!touchItem || !touchClone) return;

        touchClone.remove();
        touchItem.classList.remove("opacity-25");

        var touch  = e.changedTouches[0];
        var target = document.elementFromPoint(touch.clientX, touch.clientY);

        for (var i = 0; i < dropZones.length; i++) {
            if (dropZones[i] === target || dropZones[i].contains(target)) {
                dropZones[i].appendChild(touchItem);
                syncField(touchItem);
                syncAll();
                break;
            }
        }

        touchItem  = null;
        touchClone = null;
    });
})();
