import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Container, Grid, Paper, Typography, TextField, Button, Divider, Snackbar, Alert } from "@mui/material";
import ProfileSelector from "./components/ProfileSelector";
import AppliancesForm from "./components/AppliancesForm";
import SolarForm from "./components/SolarForm";
import AnalysisPanel from "./components/AnalysisPanel";

export default function App() {
  const [profiles, setProfiles] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [toast, setToast] = useState({ open: false, msg: "", type: "success" });

  const [newProfile, setNewProfile] = useState({
    name: "",
    location_type: "village",
    region: "",
    currency: "EUR",
    price_morning: 0.22,
    price_midday: 0.22,
    price_evening: 0.25,
    price_night: 0.18
  });

  const loadProfiles = async () => {
    const res = await axios.get("/api/profiles");
    setProfiles(res.data);
    if (!selectedId && res.data.length) setSelectedId(res.data[0].id);
  };

  useEffect(() => { loadProfiles(); }, []);

  const createProfile = async () => {
    const res = await axios.post("/api/profiles", newProfile);
    setToast({ open: true, msg: "Profil créé", type: "success" });
    await loadProfiles();
    setSelectedId(res.data.id);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 3 }}>
      <Typography variant="h4" fontWeight={800} gutterBottom>
        Agent Planificateur — Optimisation d'Énergie (Maison/Bâtiment)
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" fontWeight={700}>Profils</Typography>
            <ProfileSelector profiles={profiles} value={selectedId} onChange={setSelectedId} />

            <Divider sx={{ my: 2 }} />

            <Typography variant="subtitle1" fontWeight={700}>Créer un profil</Typography>
            <Grid container spacing={1} sx={{ mt: 1 }}>
              <Grid item xs={12}><TextField label="Nom" fullWidth value={newProfile.name} onChange={e=>setNewProfile({...newProfile, name:e.target.value})} /></Grid>
              <Grid item xs={12}><TextField label="Type (village/countryside/city)" fullWidth value={newProfile.location_type} onChange={e=>setNewProfile({...newProfile, location_type:e.target.value})} /></Grid>
              <Grid item xs={12}><TextField label="Région/Ville" fullWidth value={newProfile.region} onChange={e=>setNewProfile({...newProfile, region:e.target.value})} /></Grid>
              <Grid item xs={6}><TextField label="Prix matin" type="number" fullWidth value={newProfile.price_morning} onChange={e=>setNewProfile({...newProfile, price_morning:Number(e.target.value)})} /></Grid>
              <Grid item xs={6}><TextField label="Prix midi" type="number" fullWidth value={newProfile.price_midday} onChange={e=>setNewProfile({...newProfile, price_midday:Number(e.target.value)})} /></Grid>
              <Grid item xs={6}><TextField label="Prix soir" type="number" fullWidth value={newProfile.price_evening} onChange={e=>setNewProfile({...newProfile, price_evening:Number(e.target.value)})} /></Grid>
              <Grid item xs={6}><TextField label="Prix nuit" type="number" fullWidth value={newProfile.price_night} onChange={e=>setNewProfile({...newProfile, price_night:Number(e.target.value)})} /></Grid>
              <Grid item xs={12}><Button variant="contained" fullWidth onClick={createProfile}>Créer</Button></Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          {selectedId ? (
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <AppliancesForm profileId={selectedId} />
              </Grid>
              <Grid item xs={12}>
                <SolarForm profileId={selectedId} />
              </Grid>
              <Grid item xs={12}>
                <AnalysisPanel profileId={selectedId} />
              </Grid>
            </Grid>
          ) : (
            <Paper sx={{ p: 3 }}>
              <Typography>Créez un profil pour commencer.</Typography>
            </Paper>
          )}
        </Grid>
      </Grid>

      <Snackbar open={toast.open} autoHideDuration={2500} onClose={()=>setToast({...toast, open:false})}>
        <Alert severity={toast.type} sx={{ width: "100%" }}>{toast.msg}</Alert>
      </Snackbar>
    </Container>
  );
}
