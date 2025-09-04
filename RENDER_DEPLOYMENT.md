# Render.com Deployment Guide

This guide explains how to deploy the Football Migu backend to Render.com.

## Prerequisites

1. A Render.com account (free tier available)
2. Your code pushed to a GitHub repository
3. Vercel frontend already deployed at: `https://frontend-pgpuj3b3f-jasonyins-projects.vercel.app`

## Deployment Steps

### 1. Connect Repository to Render

1. Go to [Render.com](https://render.com) and sign in
2. Click "New +" and select "Web Service"
3. Connect your GitHub account if not already connected
4. Select your `football-migu` repository
5. Choose the `main` branch

### 2. Configure Service Settings

Render will auto-detect the `render.yaml` file and use these settings:

- **Name**: `football-migu-backend`
- **Runtime**: Python 3.11
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: `cd backend && python render_start.py`
- **Plan**: Free tier
- **Health Check Path**: `/health`

### 3. Environment Variables

The following environment variables are automatically configured via `render.yaml`:

- `HOST`: `0.0.0.0`
- `PORT`: Automatically assigned by Render
- `ENVIRONMENT`: `production`
- `DATABASE_URL`: `sqlite:///data/football_betting.db`
- `BACKEND_CORS_ORIGINS`: JSON array with Vercel frontend URLs
- `LOG_LEVEL`: `INFO`
- `DEBUG`: `false`

### 4. Additional Environment Variables (Optional)

If you need to add API keys, you can set them in the Render dashboard:

- `ANTHROPIC_API_KEY`: Your Claude/Anthropic API key
- `FOOTBALL_API_KEY`: Your football data API key

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically start the build and deployment process
3. Monitor the build logs in the Render dashboard
4. Once deployed, your backend will be available at a URL like: `https://football-migu-backend.onrender.com`

## Post-Deployment

### 1. Test the Deployment

Test your deployed backend:

```bash
# Health check
curl https://your-backend-url.onrender.com/health

# API documentation
open https://your-backend-url.onrender.com/docs
```

### 2. Update Frontend Configuration

Update your frontend configuration to use the new Render backend URL instead of the Railway URL.

In your frontend environment variables or configuration:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.onrender.com/api/v1
```

### 3. Verify CORS

Ensure your frontend can connect to the backend by checking the browser console for any CORS errors.

## Troubleshooting

### Common Issues

1. **Build fails**: Check the build logs in Render dashboard
2. **Database issues**: The SQLite database is stored in `/data` directory with persistent disk
3. **CORS errors**: Verify the frontend URL is included in `BACKEND_CORS_ORIGINS`
4. **Health check fails**: Check that `/health` endpoint is responding

### Logs

Access logs in the Render dashboard:
- Build logs: Available during deployment
- Runtime logs: Available in the "Logs" tab of your service

### Database

The SQLite database is stored on a persistent disk mounted at `/data`. This ensures your data persists across deployments.

## Configuration Files

### Key Files Created/Modified:

1. **`/Users/jasonyin/project/football-migu/render.yaml`** - Render service configuration
2. **`/Users/jasonyin/project/football-migu/backend/render_start.py`** - Render-optimized startup script
3. **`/Users/jasonyin/project/football-migu/backend/main.py`** - Updated CORS configuration
4. **`/Users/jasonyin/project/football-migu/backend/requirements.txt`** - Updated dependencies

### CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000` (local development)
- `http://localhost:3001` (local development)
- `https://frontend-pgpuj3b3f-jasonyins-projects.vercel.app` (your Vercel deployment)
- `https://football-migu.vercel.app` (potential custom domain)

## Scaling and Performance

### Free Tier Limitations:
- Service spins down after 15 minutes of inactivity
- Cold start time when waking up
- Limited CPU and memory

### Upgrade Options:
- Starter plan ($7/month) for always-on service
- Standard plan ($25/month) for better performance

## Maintenance

### Updating the Deployment:
1. Push changes to your GitHub repository
2. Render will automatically redeploy from the `main` branch
3. Monitor the deployment in the Render dashboard

### Database Backups:
- Consider implementing a backup strategy for the SQLite database
- The persistent disk ensures data survives deployments

## Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Review build and runtime logs in Render dashboard
3. Check the health endpoint: `https://your-app.onrender.com/health`