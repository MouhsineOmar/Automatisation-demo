import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Paper, Typography, Divider, Grid, Chip, List, ListItem, ListItemText } from "@mui/material";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";

export default function AnalysisPanel({ profileId }) {
  const [data, setData] = useState(null);

  const load = async () => {
    const res = await axios.get(`/api/profiles/${profileId}/analysis`);
    setData(res.data);
  };

  useEffect(()=>{ if(profileId) load(); }, [profileId]);

  const chartData = useMemo(() => {
    if (!data) return [];
    const b = data.baseline.kwh_by_period_month;
    const a = data.after.kwh_by_period_month;
    return ["morning","midday","evening","night"].map(p => ({
      period: p,
      baseline: b[p],
      after: a[p],
    }));
  }, [data]);

  if (!data) {
    return <Paper sx={{ p: 2 }}><Typography>Chargement analyse…</Typography></Paper>;
  }

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" fontWeight={800}>Analyse & Rentabilité</Typography>
      <Typography variant="body2" sx={{ opacity: 0.8 }}>
        Résultats basés sur vos appareils, vos heures d'usage, vos tarifs, et l'option solaire.
      </Typography>

      <Divider sx={{ my: 2 }} />

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Typography fontWeight={700}>Avant (mensuel)</Typography>
          <Chip label={`${data.baseline.kwh_month} kWh/mois`} sx={{ mr: 1, mt: 1 }} />
          <Chip label={`${data.baseline.cost_month} ${data.currency}/mois`} sx={{ mt: 1 }} />
          <Divider sx={{ my: 2 }} />
          <Typography fontWeight={700}>Après (avec solaire)</Typography>
          <Chip label={`${data.after.kwh_month} kWh/mois`} sx={{ mr: 1, mt: 1 }} />
          <Chip label={`${data.after.cost_month} ${data.currency}/mois`} sx={{ mt: 1 }} />
          <Divider sx={{ my: 2 }} />
          <Typography fontWeight={700}>Économies</Typography>
          <Chip color="success" label={`${data.savings.cost_savings_month} ${data.currency}/mois`} sx={{ mr: 1, mt: 1 }} />
          <Chip color="success" label={`${data.savings.cost_savings_year} ${data.currency}/an`} sx={{ mt: 1 }} />
          <Divider sx={{ my: 2 }} />
          <Typography fontWeight={700}>Rentabilité</Typography>
          <Chip label={data.savings.payback_years ? `${data.savings.payback_years} ans` : "—"} sx={{ mr: 1, mt: 1 }} />
          <Chip label={`Net 3 ans: ${data.savings.net_savings_3y} ${data.currency}`} sx={{ mr: 1, mt: 1 }} />
          <Chip label={`Net 5 ans: ${data.savings.net_savings_5y} ${data.currency}`} sx={{ mt: 1 }} />
          <Divider sx={{ my: 2 }} />
          <Typography fontWeight={700}>Solaire</Typography>
          <Typography variant="body2">
            Production: {data.solar.production_kwh_month} kWh/mois • Autoconso: {data.solar.self_consumed_kwh_month} kWh/mois • Surplus: {data.solar.excess_kwh_month} kWh/mois
          </Typography>
          <Typography variant="body2">
            Taille recommandée (pour couvrir la charge midi): <b>{data.solar.recommended_system_kwp} kWp</b>
          </Typography>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography fontWeight={700}>Conso mensuelle par période (kWh)</Typography>
          <div style={{ width: "100%", height: 260 }}>
            <ResponsiveContainer>
              <BarChart data={chartData}>
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="baseline" />
                <Bar dataKey="after" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <Divider sx={{ my: 2 }} />

          <Typography fontWeight={700}>Recommandations</Typography>
          <List dense>
            {data.recommendations.map((r, idx) => (
              <ListItem key={idx} alignItems="flex-start">
                <ListItemText primary={r.title} secondary={`${r.why} — ${r.how}`} />
              </ListItem>
            ))}
          </List>
        </Grid>
      </Grid>

      <Divider sx={{ my: 2 }} />
      <Typography fontWeight={700}>Formules</Typography>
      <Typography variant="body2">• {data.formulas.kwh_appliance}</Typography>
      <Typography variant="body2">• {data.formulas.month_factor}</Typography>
      <Typography variant="body2">• {data.formulas.solar_month}</Typography>
      <Typography variant="body2">• {data.formulas.payback}</Typography>
    </Paper>
  );
}
