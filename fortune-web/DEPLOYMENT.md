# 🔮 Zeldar Deployment Guide

## Quick Start

### Local Development
```bash
cd zeldar-fortune
spin up
# Visit http://localhost:3000
```

### Production Deployment
```bash
# Deploy to Fermyon Cloud
spin deploy

# Or deploy to custom host
spin up --listen 0.0.0.0:8080
```

## Pre-Deployment Checklist

Run the verification script:
```bash
./scripts/verify-deployment.sh
```

Expected output: ✅ All files present, ready for deployment

## Deployment Options

### 1. Fermyon Cloud (Recommended)
- **Free tier available**
- **Automatic SSL/TLS**
- **Global CDN**
- **Zero configuration**

```bash
# Install Fermyon Cloud CLI
curl -fsSL https://developer.fermyon.com/downloads/install.sh | bash

# Login to Fermyon Cloud
spin cloud login

# Deploy with custom name
spin deploy --tag v1.0
```

### 2. Self-Hosted Spin Runtime
- **Full control**
- **Custom domain**
- **Internal networks**

```bash
# Run on custom port
spin up --listen 0.0.0.0:8080

# With environment variables
SPIN_HTTP_LISTEN_ADDR=0.0.0.0:8080 spin up
```

### 3. Container Deployment
```bash
# Build container image
spin registry push

# Deploy with Docker
docker run -p 8080:8080 <your-image>
```

## Configuration

### Environment Variables
```bash
# Optional: Custom fortune refresh rate
ZELDAR_FORTUNE_REFRESH_MS=800

# Optional: Enable debug mode
ZELDAR_DEBUG=true
```

### Site Configuration
Edit `config/site.toml`:
```toml
title = "Zeldar - The Mystical Fortune-Teller"

[extra.zeldar]
fortune_style = "mystical"
historical_periods = ["mechanical", "electromechanical", "animatronic"]
```

## Performance Optimization

### WebAssembly Optimization
- **Pre-compiled**: All Rhai scripts compiled at build time
- **Minimal runtime**: ~2MB total bundle size
- **Edge deployment**: Near-zero cold start

### Content Delivery
- **Static assets**: Served directly from Spin runtime
- **Cached templates**: Handlebars pre-compiled
- **Optimized images**: WebP format recommended

### Mobile Performance
- **Responsive design**: Optimized for mobile devices
- **Touch interactions**: Finger-friendly fortune card tapping
- **Reduced motion**: Respects `prefers-reduced-motion`

## Monitoring & Analytics

### Built-in Metrics
```bash
# View deployment logs
spin cloud logs --app zeldar-fortune

# Monitor performance
spin cloud metrics --app zeldar-fortune
```

### Custom Analytics
Add to template files:
```html
<!-- Privacy-first analytics -->
<script defer data-domain="your-domain.com" src="https://plausible.io/js/script.js"></script>
```

## Security Considerations

### Content Security Policy
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
```

### HTTPS Enforcement
- **Fermyon Cloud**: Automatic HTTPS
- **Self-hosted**: Configure reverse proxy (nginx, Cloudflare)

## Troubleshooting

### Common Issues

#### 1. Rhai Script Errors
```bash
# Check script syntax
spin logs --follow
```

#### 2. Template Rendering Issues
```bash
# Validate Handlebars templates
spin doctor
```

#### 3. Static Asset 404s
- Verify files exist in `static/` directory
- Check file permissions: `chmod 644 static/**/*`

### Debug Mode
```bash
# Run with verbose logging
RUST_LOG=debug spin up
```

## Performance Benchmarks

Expected performance metrics:
- **Cold start**: <100ms
- **Page load**: <500ms
- **Fortune generation**: <50ms
- **History navigation**: <200ms

## Backup & Recovery

### Content Backup
```bash
# Backup all content
tar -czf zeldar-backup-$(date +%Y%m%d).tar.gz content/ templates/ scripts/ shortcodes/
```

### Version Control
```bash
# Tag release versions
git tag -a v1.0 -m "Zeldar Fortune-Teller v1.0"
git push origin v1.0
```

## Scaling Considerations

### Traffic Patterns
- **Fortune generation**: CPU-bound, ~10ms per request
- **History browsing**: I/O-bound, ~5ms per page
- **Static assets**: Edge-cached, ~1ms response

### Auto-scaling
Fermyon Cloud provides automatic scaling based on:
- Request volume
- Response time
- Resource utilization

---

## 🎭 Mystical Deployment Ritual

Before deploying, perform the traditional automaton blessing:

1. **Inspect the gears** - Run verification script ✅
2. **Align the cam shafts** - Check configuration files ✅  
3. **Charge the solenoids** - Test fortune generation ✅
4. **Calibrate the mechanisms** - Verify responsive design ✅
5. **Release the mystical energy** - Execute deployment 🚀

*"Like the 1957 Genco Gypsy Grandma, may your deployment achieve mechanical perfection and mystical wonder."*

## Support

- **Issues**: Create GitHub issue with deployment logs
- **Questions**: Check bartholomew.wasm and Spin documentation
- **Updates**: Follow semantic versioning for releases

---

**✨ The mechanical spirits await your successful deployment! ✨**