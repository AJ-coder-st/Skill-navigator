# Frontend Fix Commands

## Step 1: Clean Install

```powershell
cd "D:\PROJECTS\Career Readiness Mentor & Skill-Gap Navigator\frontend"
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json
npm install
```

## Step 2: Verify Vite Installation

```powershell
npm list vite
```

Should show: `vite@5.0.8` or similar

## Step 3: Test Frontend

```powershell
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Alternative: Use npx (if issues persist)

Update package.json scripts to:
```json
"dev": "npx vite",
"build": "npx vite build",
"preview": "npx vite preview"
```
