import React from "react";
import { Link } from "react-router-dom";
import { Card, CardActionArea, Box, Typography, Paper } from "@mui/material";

interface CardProps {
  cardHeight: number;
  title: string;
  linkTo: string;
}

const CustomCard: React.FC<CardProps> = ({ title, linkTo, cardHeight }) => {
  return (
    <Paper>
      <Card>
        <CardActionArea component={Link} to={linkTo}>
          <Box
            width="100%"
            height={cardHeight}
            bgcolor="grey.300"
            position="relative"
          >
            {/* Add your content or image here */}
            <Typography
              variant="h5"
              sx={{
                position: "absolute",
                bottom: 16,
                left: 16,
                color: "white",
              }}
            >
              {title}
            </Typography>
          </Box>
        </CardActionArea>
      </Card>
    </Paper>
  );
};

export default CustomCard;
