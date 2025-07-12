/**
 * Plan Viewer Module for PGI-IA Dashboard
 * Provides zoom, pan, and marker management for technical plans
 */

class PlanViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.state = {
            scale: 1,
            translateX: 0,
            translateY: 0,
            isDragging: false,
            startX: 0,
            startY: 0,
            markers: [],
            markersVisible: true,
            minScale: 0.5,
            maxScale: 5
        };
        
        this.init();
    }
    
    init() {
        if (!this.container) return;
        
        // Create wrapper structure
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'relative w-full h-full overflow-hidden cursor-grab';
        this.wrapper.style.userSelect = 'none';
        
        // Move existing content into wrapper
        while (this.container.firstChild) {
            this.wrapper.appendChild(this.container.firstChild);
        }
        this.container.appendChild(this.wrapper);
        
        // Find or create image element
        this.image = this.wrapper.querySelector('img');
        if (this.image) {
            this.image.style.transformOrigin = 'center center';
            this.image.style.position = 'absolute';
            this.image.style.width = '100%';
            this.image.style.height = '100%';
        }
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Apply initial transform
        this.updateTransform();
    }
    
    setupEventListeners() {
        // Mouse events for panning
        this.wrapper.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));
        
        // Wheel event for zooming
        this.wrapper.addEventListener('wheel', this.handleWheel.bind(this));
        
        // Touch events for mobile
        this.wrapper.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.wrapper.addEventListener('touchmove', this.handleTouchMove.bind(this));
        this.wrapper.addEventListener('touchend', this.handleTouchEnd.bind(this));
        
        // Prevent context menu
        this.wrapper.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    handleMouseDown(e) {
        if (e.button !== 0) return; // Only left mouse button
        
        this.state.isDragging = true;
        this.state.startX = e.clientX - this.state.translateX;
        this.state.startY = e.clientY - this.state.translateY;
        this.wrapper.style.cursor = 'grabbing';
        
        e.preventDefault();
    }
    
    handleMouseMove(e) {
        if (!this.state.isDragging) return;
        
        this.state.translateX = e.clientX - this.state.startX;
        this.state.translateY = e.clientY - this.state.startY;
        this.updateTransform();
    }
    
    handleMouseUp() {
        this.state.isDragging = false;
        this.wrapper.style.cursor = 'grab';
    }
    
    handleWheel(e) {
        e.preventDefault();
        
        const delta = e.deltaY > 0 ? 0.9 : 1.1;
        const newScale = Math.max(this.state.minScale, Math.min(this.state.maxScale, this.state.scale * delta));
        
        if (newScale === this.state.scale) return;
        
        // Calculate zoom point
        const rect = this.wrapper.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Adjust translation to zoom on cursor position
        const dx = (x - this.state.translateX) * (1 - delta);
        const dy = (y - this.state.translateY) * (1 - delta);
        
        this.state.scale = newScale;
        this.state.translateX += dx;
        this.state.translateY += dy;
        
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    handleTouchStart(e) {
        if (e.touches.length === 1) {
            // Single touch - pan
            const touch = e.touches[0];
            this.state.isDragging = true;
            this.state.startX = touch.clientX - this.state.translateX;
            this.state.startY = touch.clientY - this.state.translateY;
        } else if (e.touches.length === 2) {
            // Two touches - pinch zoom
            this.handlePinchStart(e);
        }
        e.preventDefault();
    }
    
    handleTouchMove(e) {
        if (e.touches.length === 1 && this.state.isDragging) {
            const touch = e.touches[0];
            this.state.translateX = touch.clientX - this.state.startX;
            this.state.translateY = touch.clientY - this.state.startY;
            this.updateTransform();
        } else if (e.touches.length === 2) {
            this.handlePinchMove(e);
        }
        e.preventDefault();
    }
    
    handleTouchEnd(e) {
        this.state.isDragging = false;
        this.state.isPinching = false;
    }
    
    handlePinchStart(e) {
        const touch1 = e.touches[0];
        const touch2 = e.touches[1];
        
        this.state.isPinching = true;
        this.state.pinchStartDistance = Math.hypot(
            touch2.clientX - touch1.clientX,
            touch2.clientY - touch1.clientY
        );
        this.state.pinchStartScale = this.state.scale;
    }
    
    handlePinchMove(e) {
        if (!this.state.isPinching) return;
        
        const touch1 = e.touches[0];
        const touch2 = e.touches[1];
        
        const currentDistance = Math.hypot(
            touch2.clientX - touch1.clientX,
            touch2.clientY - touch1.clientY
        );
        
        const scale = (currentDistance / this.state.pinchStartDistance) * this.state.pinchStartScale;
        this.state.scale = Math.max(this.state.minScale, Math.min(this.state.maxScale, scale));
        
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    updateTransform() {
        if (!this.image) return;
        
        const transform = `translate(${this.state.translateX}px, ${this.state.translateY}px) scale(${this.state.scale})`;
        this.image.style.transform = transform;
        
        // Also transform markers container if it exists
        const markersContainer = this.wrapper.querySelector('.markers-container');
        if (markersContainer) {
            markersContainer.style.transform = transform;
        }
    }
    
    // Public methods
    zoomIn() {
        this.state.scale = Math.min(this.state.scale * 1.2, this.state.maxScale);
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    zoomOut() {
        this.state.scale = Math.max(this.state.scale / 1.2, this.state.minScale);
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    resetView() {
        this.state.scale = 1;
        this.state.translateX = 0;
        this.state.translateY = 0;
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    fitToContainer() {
        if (!this.image) return;
        
        const containerRect = this.wrapper.getBoundingClientRect();
        const imgRect = this.image.getBoundingClientRect();
        
        const scaleX = containerRect.width / imgRect.width;
        const scaleY = containerRect.height / imgRect.height;
        
        this.state.scale = Math.min(scaleX, scaleY) * 0.9; // 90% to add some padding
        this.state.translateX = 0;
        this.state.translateY = 0;
        
        this.updateTransform();
        this.onZoomChange(this.state.scale);
    }
    
    getZoomLevel() {
        return Math.round(this.state.scale * 100);
    }
    
    // Override this method to handle zoom changes
    onZoomChange(scale) {
        // Can be overridden by users of this class
        const event = new CustomEvent('zoomchange', { 
            detail: { scale: scale, percentage: this.getZoomLevel() }
        });
        this.container.dispatchEvent(event);
    }
    
    // Marker management
    addMarker(x, y, options = {}) {
        const marker = {
            id: Date.now(),
            x: x,
            y: y,
            ...options
        };
        
        this.state.markers.push(marker);
        this.renderMarkers();
        return marker.id;
    }
    
    removeMarker(id) {
        this.state.markers = this.state.markers.filter(m => m.id !== id);
        this.renderMarkers();
    }
    
    clearMarkers() {
        this.state.markers = [];
        this.renderMarkers();
    }
    
    renderMarkers() {
        // Implementation depends on specific marker rendering needs
        // This is a placeholder for the actual implementation
    }
}

// Export for use in dashboard
window.PlanViewer = PlanViewer;