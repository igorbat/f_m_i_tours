from abaka.abaka_cls import *
import unittest


class TestSolve(unittest.TestCase):
    def get_player1(self):
        pl = Player(1, "1s")
        return pl

    def get_1t(self):
        tour_1t = GameAbaka("1t", "link", [["1",["1"],["1"]],
                                           ["2",["1"],["1"]]])
        return tour_1t

    def test_solve(self):
        sm = StateMachine()
        sm.register_player("1", "1", "ls")
        sm.add_tour("1t", self.get_1t())
        sm.join_tour("1", "1t")
        sm.solve("1", "1", "1", "1")

        self.assertEqual(sm.players["1"].tours["1t"][4], 10)

        sm.solve("1", "1", "2", "1")

        self.assertEqual(sm.players["1"].tours["1t"][4], 10 + 20 + 50 * 2)

        sm.register_player("2", "1", "ls")
        sm.join_tour("2", "1t")
        sm.solve("2", "1", "1", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10)

        sm.solve("2", "1", "2", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50)

        sm.solve("2", "2", "1", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50 + 10 + 10*2)

        ok, msg = sm.solve("2", "2", "2", "1")

        self.assertEqual(sm.players["2"].tours["1t"][4], 10 + 20 + 50 + 10 + 10 * 2 + 20 + 50 * 2 + 20 * 2)
        self.assertEqual("Ответ совпал! Теперь у вас {}".format(10 + 20 + 50 + 10 + 10 * 2 + 20 + 50 * 2 + 20 * 2), msg)

    def test_sort(self):
        sm = StateMachine()
        sm.register_player("1", "1", "1s")
        sm.register_player("2", "2", "2s")
        sm.register_player("3", "3", "3s")
        sm.add_tour("1t", GameAbaka("1t", "link", [["1", ["1"], ["1"]], ["2", ["1"], ["1"]]]))
        sm.add_tour("2t", GameAbaka("2t", "link", [["1", ["1"], ["1"]], ["2", ["1"], ["1"]]]))

        sm.join_tour("1", "2t")
        sm.join_tour("2", "2t")
        sm.join_tour("3", "2t")

        for player in sm.players.values():
            player.current_tour = None

        sm.join_tour("1", "1t")
        sm.join_tour("2", "1t")
        sm.join_tour("3", "1t")

        sm.solve("2", "2", "1", "1")
        sm.solve("1", "2", "1", "1")
        sm.solve("2", "1", "1", "1")
        sm.solve("1", "1", "1", "1")
        sm.solve("2", "2", "2", "2")

        vls = sm.get_sorted_res()
        for vll in vls:
            if vll[0] == "1t":
                self.assertEqual(vll[1][0][0], "2_2s-1")
                self.assertEqual(vll[1][1][0], "1_1s-1")
                self.assertEqual(vll[1][2][0], "3_3s-1")
            if vll[0] == "2t":
                self.assertEqual(vll[1][0][0], "1_1s-1")
                self.assertEqual(vll[1][1][0], "2_2s-1")
                self.assertEqual(vll[1][2][0], "3_3s-1")
        sm.reload_res()
