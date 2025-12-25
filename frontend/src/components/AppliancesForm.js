import React, { useEffect, useState } from "react";
import axios from "axios";
import { Paper, Typography, Grid, TextField, Button, Divider, Table, TableHead, TableRow, TableCell, TableBody } from "@mui/material";

export default function AppliancesForm({ profileId }) {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    name: "",
    category: "lamp",
    power_watts: 60,
    quantity: 1,
    h_morning: 0,
    h_midday: 0,
    h_evening: 0,
    h_night: 0,
    days_per_week: 7
  });

  const load = async () => {
    const res = await axios.get(`/api/profiles/${profileId}/appliances`);
    setItems(res.data);
  };

  useEffect(()=>{ if(profileId) load(); }, [profileId]);

  const add = async () => {
    await axios.post(`/api/profiles/${profileId}/appliances`, form);
    await load();
    setForm({ ...form, name: "" });
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" fontWeight={800}>Appareils & usages</Typography>
      <Typography variant="body2" sx={{ opacity: 0.8 }}>
        Ajoutez lampes, clim, frigo… avec puissance (W), quantité, et heures d'usage par période.
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={1}>
        <Grid item xs={12} md={6}><TextField label="Nom" fullWidth value={form.name} onChange={e=>setForm({...form, name:e.target.value})} /></Grid>
        <Grid item xs={12} md={6}><TextField label="Catégorie (lamp/ac/fridge/...)" fullWidth value={form.category} onChange={e=>setForm({...form, category:e.target.value})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Puissance (W)" type="number" fullWidth value={form.power_watts} onChange={e=>setForm({...form, power_watts:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Quantité" type="number" fullWidth value={form.quantity} onChange={e=>setForm({...form, quantity:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Jours/sem." type="number" fullWidth value={form.days_per_week} onChange={e=>setForm({...form, days_per_week:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><Button variant="contained" fullWidth sx={{ height: "100%" }} onClick={add}>Ajouter</Button></Grid>

        <Grid item xs={6} md={3}><TextField label="Heures matin" type="number" fullWidth value={form.h_morning} onChange={e=>setForm({...form, h_morning:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Heures midi" type="number" fullWidth value={form.h_midday} onChange={e=>setForm({...form, h_midday:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Heures soir" type="number" fullWidth value={form.h_evening} onChange={e=>setForm({...form, h_evening:Number(e.target.value)})} /></Grid>
        <Grid item xs={6} md={3}><TextField label="Heures nuit" type="number" fullWidth value={form.h_night} onChange={e=>setForm({...form, h_night:Number(e.target.value)})} /></Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />

      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Cat.</TableCell>
            <TableCell align="right">W</TableCell>
            <TableCell align="right">Qty</TableCell>
            <TableCell align="right">Matin</TableCell>
            <TableCell align="right">Midi</TableCell>
            <TableCell align="right">Soir</TableCell>
            <TableCell align="right">Nuit</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map(a => (
            <TableRow key={a.id}>
              <TableCell>{a.name}</TableCell>
              <TableCell>{a.category}</TableCell>
              <TableCell align="right">{a.power_watts}</TableCell>
              <TableCell align="right">{a.quantity}</TableCell>
              <TableCell align="right">{a.h_morning}</TableCell>
              <TableCell align="right">{a.h_midday}</TableCell>
              <TableCell align="right">{a.h_evening}</TableCell>
              <TableCell align="right">{a.h_night}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
