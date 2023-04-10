package java;

class findMaxConsecutiveOnes {
    public int solution(int[] nums) {
        
        int mainCount = 0;
        int subCount = 0;
        for (int i = 0; i < nums.length; i++){
            if(nums[i]==0){
                subCount = 0;
            }else{
                subCount+=1;
            }
            if(mainCount < subCount){
                mainCount = subCount;
            }
        }
        return mainCount;
    }
}