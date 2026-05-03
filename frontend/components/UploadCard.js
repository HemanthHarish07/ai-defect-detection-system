import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Typography,
} from "@mui/material";
import { uploadImage } from "../services/api";

export default function UploadCard({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage("Please select an image file.");
      return;
    }
    setLoading(true);
    try {
      await uploadImage(file);
      setMessage("Upload successful. Predictions are updated.");
      setFile(null);
      onUploaded?.();
    } catch (error) {
      setMessage(error?.response?.data?.detail || "Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Upload Product Image
        </Typography>
        <Box display="flex" flexDirection="column" gap={2}>
          <input type="file" accept="image/png,image/jpeg" onChange={handleFileChange} />
          {loading && <LinearProgress />}
          <Button variant="contained" onClick={handleSubmit} disabled={loading}>
            Submit Image
          </Button>
          {message && <Typography color="text.secondary">{message}</Typography>}
        </Box>
      </CardContent>
    </Card>
  );
}
