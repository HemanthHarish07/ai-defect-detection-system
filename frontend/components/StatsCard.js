import { Card, CardContent, Typography } from "@mui/material";

export default function StatsCard({ label, value, color }) {
  return (
    <Card sx={{ borderLeft: 6, borderColor: `${color}.main` }}>
      <CardContent>
        <Typography variant="subtitle2" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="h4" color={color + ".main"}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}
