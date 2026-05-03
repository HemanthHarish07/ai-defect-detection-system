import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Grid,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import UploadCard from "../components/UploadCard";
import StatsCard from "../components/StatsCard";
import { fetchHistory } from "../services/api";

export default function Home() {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    defective: 0,
    non_defective: 0,
  });
  const [refreshing, setRefreshing] = useState(false);

  const loadDashboard = async () => {
    setRefreshing(true);

    const historyRes = await fetchHistory();
    const data = historyRes.events || historyRes;

    console.log("HISTORY:", data); // debug

    setHistory(data);

    // ✅ FIXED LOGIC (BASED ON CONFIDENCE)
    const total = data.length;

    const defective = data.filter(
      (item) => Number(item.confidence) < 0.5
    ).length;

    const non_defective = data.filter(
      (item) => Number(item.confidence) >= 0.5
    ).length;

    console.log("STATS:", { total, defective, non_defective });

    setStats({
      total,
      defective,
      non_defective,
    });

    setRefreshing(false);
  };

  useEffect(() => {
    loadDashboard();
    const interval = setInterval(loadDashboard, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box
      sx={{
        background: "linear-gradient(135deg, #eef2f7, #f9fbfd)",
        minHeight: "100vh",
        py: 5,
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="h4" fontWeight={700} gutterBottom>
          🚀 Automated Defect Detection
        </Typography>
        <Typography variant="body1" color="text.secondary" mb={4}>
          AI-powered real-time manufacturing quality analysis
        </Typography>

        <Grid container spacing={3}>
          {/* Upload */}
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
              <CardContent>
                <UploadCard onUploaded={loadDashboard} />
              </CardContent>
            </Card>
          </Grid>

          {/* Stats */}
          <Grid item xs={12} md={6}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <StatsCard label="Total" value={stats.total} color="primary" />
              </Grid>
              <Grid item xs={12} sm={6}>
                <StatsCard label="Defective" value={stats.defective} color="error" />
              </Grid>
              <Grid item xs={12} sm={6}>
                <StatsCard
                  label="Non-defective"
                  value={stats.non_defective}
                  color="success"
                />
              </Grid>
            </Grid>
          </Grid>

          {/* Table */}
          <Grid item xs={12}>
            <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
              <CardContent>
                <Box
                  display="flex"
                  alignItems="center"
                  justifyContent="space-between"
                  mb={2}
                >
                  <Typography variant="h6" fontWeight={600}>
                    📊 Recent Defect History
                  </Typography>
                  {refreshing && <CircularProgress size={20} />}
                </Box>

                <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
                  <Table>
                    <TableHead>
                      <TableRow sx={{ backgroundColor: "#f1f5f9" }}>
                        <TableCell sx={{ fontWeight: 600 }}>Filename</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Confidence</TableCell>
                        <TableCell sx={{ fontWeight: 600 }}>Timestamp</TableCell>
                      </TableRow>
                    </TableHead>

                    <TableBody>
                      {history.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={4} align="center">
                            No data yet — upload image 🚀
                          </TableCell>
                        </TableRow>
                      ) : (
                        history.map((item) => (
                          <TableRow key={item.id} hover>
                            <TableCell>{item.filename}</TableCell>

                            {/* ✅ FIXED STATUS */}
                            <TableCell
                              sx={{
                                color:
                                  item.confidence < 0.5
                                    ? "error.main"
                                    : "success.main",
                                fontWeight: 600,
                              }}
                            >
                              {item.confidence < 0.5
                                ? "defective"
                                : "non_defective"}
                            </TableCell>

                            <TableCell>
                              {(Math.min(item.confidence, 1) * 100).toFixed(1)}%
                            </TableCell>

                            <TableCell>
                              {new Date(item.uploaded_at).toLocaleString()}
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}