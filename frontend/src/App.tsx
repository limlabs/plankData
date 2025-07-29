import { useState, useEffect } from 'react'
import { Box, Slider, Typography, Container, Paper, Tabs, Tab, ThemeProvider, createTheme } from '@mui/material'
import axios from 'axios'

const theme = createTheme({
  palette: {
    mode: 'light',
  },
})

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

interface ParamRange {
  min: number;
  max: number;
  step: number;
}

interface HilltopParams extends Record<string, number> {
  amp: number;
  mu: number;
  v: number;
  p: number;
  phi: number;
}

interface StarobinskyParams extends Record<string, number> {
  amp: number;
  decay: number;
  phase: number;
  freq: number;
  supp: number;
}

const renderSliders = <T extends Record<string, number>>(
  params: T,
  setParams: React.Dispatch<React.SetStateAction<T>>,
  ranges: { [K in keyof T]: ParamRange }
) => {
  const entries = Object.entries(params);
  const midPoint = Math.ceil(entries.length / 2);
  const leftColumn = entries.slice(0, midPoint);
  const rightColumn = entries.slice(midPoint);

  return (
    <Box sx={{ display: 'flex', gap: 6 }}>
      <Box sx={{ flex: 1 }}>
        {leftColumn.map(([key, value]) => (
          <Box key={key} sx={{ mb: 3 }}>
            <Typography sx={{ mb: 1 }}>
              {key}: {value}
            </Typography>
            <Slider
              value={value}
              onChange={(_, newValue) => {
                setParams(prev => ({ ...prev, [key]: newValue as number }))
              }}
              min={ranges[key].min}
              max={ranges[key].max}
              step={ranges[key].step}
              marks={[
                { value: ranges[key].min, label: ranges[key].min.toString() },
                { value: ranges[key].max, label: ranges[key].max.toString() }
              ]}
            />
          </Box>
        ))}
      </Box>
      <Box sx={{ flex: 1 }}>
        {rightColumn.map(([key, value]) => (
          <Box key={key} sx={{ mb: 3 }}>
            <Typography sx={{ mb: 1 }}>
              {key}: {value}
            </Typography>
            <Slider
              value={value}
              onChange={(_, newValue) => {
                setParams(prev => ({ ...prev, [key]: newValue as number }))
              }}
              min={ranges[key].min}
              max={ranges[key].max}
              step={ranges[key].step}
              marks={[
                { value: ranges[key].min, label: ranges[key].min.toString() },
                { value: ranges[key].max, label: ranges[key].max.toString() }
              ]}
            />
          </Box>
        ))}
      </Box>
    </Box>
  );
};

function App() {
  const [activeTab, setActiveTab] = useState(2);  // Start with Starobinsky model
  const [standardImage, setStandardImage] = useState('')
  const [hilltopImage, setHilltopImage] = useState('')
  const [starobinskyImage, setStarobinskyImage] = useState('')

  // Hilltop model parameters with ranges
  const [hilltopParams, setHilltopParams] = useState<HilltopParams>({
    amp: 4700,  // Range: 1000-10000
    mu: 13.5,   // Range: 10-20
    v: 1.8,     // Range: 0.1-5
    p: 3.2,     // Range: 2-10
    phi: 0.37   // Range: 0.1-1
  })

  // Starobinsky model parameters with ranges
  const [starobinskyParams, setStarobinskyParams] = useState<StarobinskyParams>({
    amp: 5500,   // Range: 1000-10000
    decay: 9000, // Range: 5000-15000
    phase: 4.0,  // Range: 0-10
    freq: 0.95,  // Range: 0.1-2
    supp: 0.07   // Range: 0.01-0.2
  })

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  // Fetch standard model
  useEffect(() => {
    axios.get('/api/standard', { responseType: 'blob' })
      .then(response => {
        setStandardImage(URL.createObjectURL(response.data))
      })
      .catch(error => console.error('Error fetching standard model:', error))
  }, [])

  // Fetch Hilltop model
  useEffect(() => {
    const params = new URLSearchParams()
    Object.entries(hilltopParams).forEach(([key, value]) => {
      params.append(key, value.toString())
    })
    axios.get(`/api/hilltop?${params}`, { responseType: 'blob' })
      .then(response => {
        setHilltopImage(URL.createObjectURL(response.data))
      })
      .catch(error => console.error('Error fetching hilltop model:', error))
  }, [hilltopParams])

  // Fetch Starobinsky model
  useEffect(() => {
    const params = new URLSearchParams()
    Object.entries(starobinskyParams).forEach(([key, value]) => {
      params.append(key, value.toString())
    })
    axios.get(`/api/starobinsky?${params}`, { responseType: 'blob' })
      .then(response => {
        setStarobinskyImage(URL.createObjectURL(response.data))
      })
      .catch(error => console.error('Error fetching starobinsky model:', error))
  }, [starobinskyParams])

  const paramRanges = {
    hilltop: {
      amp: { min: 1000, max: 10000, step: 100 },
      mu: { min: 10, max: 20, step: 0.1 },
      v: { min: 0.1, max: 5, step: 0.1 },
      p: { min: 2, max: 10, step: 0.1 },
      phi: { min: 0.1, max: 1, step: 0.01 }
    },
    starobinsky: {
      amp: { min: 1000, max: 10000, step: 100 },
      decay: { min: 5000, max: 15000, step: 100 },
      phase: { min: 0, max: 10, step: 0.1 },
      freq: { min: 0.1, max: 2, step: 0.01 },
      supp: { min: 0.01, max: 0.2, step: 0.01 }
    }
  };

  return (
    <ThemeProvider theme={theme}>
    <Container maxWidth="lg" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 1 }}>
      <Box sx={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
        <Typography variant="h5" component="h1" sx={{ mb: 1 }} align="center">
          CMB Power Spectrum Models
        </Typography>
        
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={activeTab} onChange={handleTabChange} centered>
            <Tab label="Standard ΛCDM" />
            <Tab label="Hilltop Inflation" />
            <Tab label="Starobinsky R² Inflation" />
          </Tabs>
        </Box>

        <TabPanel value={activeTab} index={0}>
          <Box sx={{ flexGrow: 1 }}>
            <Paper sx={{ p: 1.5, mb: 1 }}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>Standard ΛCDM Model</Typography>
              {standardImage && <img src={standardImage} alt="Standard Model" style={{width: '100%'}} />}
            </Paper>
          </Box>
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <Paper sx={{ p: 1.5, mb: 1 }}>
            <Typography variant="h6" gutterBottom>Hilltop Inflation Model</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
                {hilltopImage && <img src={hilltopImage} alt="Hilltop Model" style={{maxWidth: '100%', height: '450px', objectFit: 'contain'}} />}
              </Box>
              <Box sx={{ width: '100%' }}>
                {renderSliders<HilltopParams>(hilltopParams, setHilltopParams, paramRanges.hilltop)}
              </Box>
            </Box>
          </Paper>
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <Paper sx={{ p: 1.5, mb: 1 }}>
            <Typography variant="h6" gutterBottom>Starobinsky R² Inflation Model</Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
                {starobinskyImage && <img src={starobinskyImage} alt="Starobinsky Model" style={{maxWidth: '100%', height: '450px', objectFit: 'contain'}} />}
              </Box>
              <Box sx={{ width: '100%' }}>
                {renderSliders<StarobinskyParams>(starobinskyParams, setStarobinskyParams, paramRanges.starobinsky)}
              </Box>
            </Box>
          </Paper>
        </TabPanel>
      </Box>
    </Container>
    </ThemeProvider>
  )
}

export default App
