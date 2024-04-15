import { Link } from "react-router-dom";
import {
  Card,
  CardActionArea,
  Box,
  Typography,
  Paper,
  alpha,
} from "@mui/material";
import { ReactNode } from "react";

interface CardProps {
  cardHeight: number;
  title: string;
  linkTo: string;
  component: ReactNode;
}

const CustomCard = ({ title, linkTo, cardHeight, component }: CardProps) => {
  return (
    <Paper>
      <Card>
        <CardActionArea component={Link} to={linkTo}>
          <Box
            width="100%"
            height={cardHeight}
            position="relative"
            sx={{
              backgroundColor: alpha("#808080", 0.5),
            }}
          >
            {component}

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
