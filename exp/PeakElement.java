public class PeakElement {

    // Function to find a peak element index using binary search
    public static int findPeakElement(int[] nums) {
        int left = 0, right = nums.length - 1;

        while (left < right) {
            int mid = left + (right - left) / 2;

            // Compare mid with its next neighbor
            if (nums[mid] > nums[mid + 1]) {
                // You are in the decreasing part of the array
                // So the peak is on the left including mid
                right = mid;
            } else {
                // You are in the increasing part of the array
                // So the peak is on the right (mid+1 to right)
                left = mid + 1;
            }
        }

        // When left == right, we have found a peak
        return left;
    }

    // Main method to test the code
    public static void main(String[] args) {
        int[] nums = {1, 3, 20, 4, 1, 0};

        int peakIndex = findPeakElement(nums);
        System.out.println("Peak element is at index: " + peakIndex);
        System.out.println("Peak element value: " + nums[peakIndex]);
    }
}
