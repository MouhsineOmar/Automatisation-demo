import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

export default function ProfileSelector({ profiles, value, onChange }) {
  return (
    <FormControl fullWidth size="small" sx={{ mt: 1 }}>
      <InputLabel>Profil</InputLabel>
      <Select value={value ?? ""} label="Profil" onChange={(e)=>onChange(e.target.value)}>
        {profiles.map(p => (
          <MenuItem key={p.id} value={p.id}>{p.name} — {p.location_type}</MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
