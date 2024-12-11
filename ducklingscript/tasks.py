from .compiler.sourcemapping.base64vlq import vlq_encode, vlq_decode


def base64vlq_encode(nums: str):
    separated_nums = nums.split(",")
    try:
        numbers = [int(num.strip()) for num in separated_nums]
    except ValueError:
        print("The numbers given were not valid.")
        return
    print(f"-> {vlq_encode(*numbers)}")


def base64vlq_decode(text: str):
    print(f"-> {vlq_decode(text)}")
