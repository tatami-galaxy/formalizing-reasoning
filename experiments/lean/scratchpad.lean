#eval String.append "Hello" " Lean"
#eval String.append "it is " (if 1 > 2 then "yes" else "no")
#eval (1 + 2 : Nat)
#eval (1 - 2 : Int)

def add1 (n : Nat) : Nat := n + 1

#eval add1 5

def spaceBetween (before : String) (after : String) : String :=
  String.append before (String.append " " after)

#eval spaceBetween "hello" "world"

#check spaceBetween

structure Point where
  x : Float
  y : Float
deriving Repr

def origin : Point := { x := 0.0, y := 0.0 }

#eval origin.x

def addPoints (p1 : Point) (p2 : Point) : Point :=
  { x := p1.x + p2.x, y := p1.y + p2.y }

#eval addPoints { x := 1.5, y := 32 } { x := -8, y := 0.2 }

#check fun(x : Nat) => x + 5

#check Nat.add
#check Nat.add 5

def α : Type := Nat
#check α

#eval (λ x y : Nat => x + y ) 10 12


set_option linter.unusedVariables false
---
variable {p : Prop}
variable {q : Prop}

theorem t1 : p → q → p := fun hp : p => fun hq : q => hp

#print t1

theorem t2 : p → q → p :=
  fun hp : p =>
  fun hq : q =>
  show p from hp

#print t2

#check 2 + 2 = 4

#check p ∨ q

example (hp : p) (hq : q) : p ∧ q := And.intro hp hq
