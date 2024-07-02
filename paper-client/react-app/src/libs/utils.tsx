import { LastPageTwoTone } from "@mui/icons-material";

export const getLastKeyFromURL = (path: string): string => {
    const segments = path.split('/'); // パスをスラッシュで分割
    return segments[segments.length - 1]; // 最後のセグメントを返す（キー）
};

export const getLastTwoKeyFromURL = (path: string): string[] => {
    const segments = path.split('/'); // パスをスラッシュで分割
    return segments.slice(-2)
};
