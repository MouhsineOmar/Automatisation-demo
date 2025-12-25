import React, { useEffect, useState } from "react";
import axios from "axios";
import { Paper, Typography, Grid, TextField, Button, Divider } from "@mui/material";

export default function SolarForm({ profileId }) {
  const [solar, setSolar] = useState({
    system_size_kwp: 0,
    install_cost: 0,
    peak_sun_hours_midday: 4.0,
    performance_ratio: 0.75
  });

  const load = async () => {
    const res = await axios.get(`/api/profiles/${profileId}/solar`);
    if (res.data) setSolar(res.data);
  };

  useEffect(()=>{ if(profileId) load(); }, [profileId]);

  const save = async () => {
    await axios.post(`/api/profiles/${profileId}/solar`, solar);
    await load();
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" fontWeight={800}>Solaire (optionnel)</Typography>
      <Typography variant="body2" sx={{ opacity: 0.8 }}>
        Configurez la taille (kWp) et le coût. PSH (heures solaires) et PR (rendement) permettent un calcul réaliste.
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={1}>
        <Grid item xs={6} md={3}><TextField label="kWp" type="number" fullWidth value={solar.system_size_kwp} onChange={e=>setSolar({...solar, system_size_kwp:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Coût installation" type="number" fullWidth value={solar.install_cost} onChange={e=>setSolar({...solar, install_cost:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="PSH (midi)" type="number" fullWidth value={solar.peak_sun_hours_midday} onChange={e=>setSolar({...solar, peak_sun_hours_midday:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="PR" type="number" fullWidth value={solar.performance_ratio} onChange={e=>setSolar({...solar, performance_ratio:Number(e.target.value)})} /></Grid>
        <Grid item xs={12}><Button variant="contained" fullWidth onClick={save}>Enregistrer solaire</Button></Grid>
      </Grid>
    </Paper>
  );
}
