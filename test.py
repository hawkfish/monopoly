import copy
import monopoly
import unittest

class TestMonopoly(unittest.TestCase):

    def setUp(self):
        pass

    def _testDrawCard(self, cards):
        expected = copy.copy(cards)
        actual = []
        for c in range(0,len(cards)):
            actual.append(monopoly.drawCard(cards))
        
        self.assertEqual(expected, actual)

    def testDrawChance(self):
        self._testDrawCard(monopoly.chanceCards)

    def testDrawCommunityChest(self):
        self._testDrawCard(monopoly.communityChestCards)

    def testDrawOneCard(self):
        self._testDrawCard([monopoly.AdvanceToUtility,])
        
    def _prepareCards(self, cards, card):
        while cards[0] != card:
            monopoly.drawCard(cards)
    
    def _testMove(self, expected, setup, d1, d2, chance = monopoly.DontMove, communityChest = monopoly.DontMove):
        self._prepareCards(monopoly.chanceCards, chance)
        self._prepareCards(monopoly.communityChestCards, communityChest)
        
        actual = copy.copy(setup)
        actual.move(d1, d2)
        self.assertEqual(expected.token, actual.token)
        self.assertEqual(expected.doubles, actual.doubles)
        self.assertEqual(expected.jail, actual.jail)
        self.assertEqual(expected.trips, actual.trips)
        self.assertEqual(expected.turns, actual.turns)
    
    def testRollFromGo(self):
        setup = monopoly.Player()
        expected = monopoly.Player(1, monopoly.Reading)
        self._testMove(expected, setup, 2, 3)

    def testDoublesFromGo(self):
        setup = monopoly.Player()
        expected = monopoly.Player(0, 6, 1)
        self._testMove(expected, setup, 3, 3)

    def testDoublesAheadToJail(self):
        setup = monopoly.Player(0, 6, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 3, 3)

    def testDoublesBackToJail(self):
        setup = monopoly.Player(0, 16, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 3, 3)

    def testGoToJail(self):
        setup = monopoly.Player(0, 21, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 5)

    def testGoToJailFirstDoubles(self):
        setup = monopoly.Player(0, 22, 0)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 4)

    def testGoToJailSecondDoubles(self):
        setup = monopoly.Player(0, 22, 1)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 4)

    def testGoToJailThirdDoubles(self):
        setup = monopoly.Player(0, 22, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 4)

    def testJailFirstRoll(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 0)
        expected = monopoly.Player(1, monopoly.Jail, 0, 1)
        self._testMove(expected, setup, 4, 5)

    def testJailSecondRoll(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 1)
        expected = monopoly.Player(1, monopoly.Jail, 0, 2)
        self._testMove(expected, setup, 4, 5)

    def testJailThirdRoll(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 2)
        expected = monopoly.Player(1, 19, 0, 3)
        self._testMove(expected, setup, 4, 5)

    def testJailFirstRollDoubles(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 0)
        expected = monopoly.Player(1, 18, 0, 3)
        self._testMove(expected, setup, 4, 4)

    def testJailSecondRollDoubles(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 1)
        expected = monopoly.Player(1, 18, 0, 3)
        self._testMove(expected, setup, 4, 4)

    def testJailThirdRollDoubles(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 2)
        expected = monopoly.Player(1, 18, 0, 3)
        self._testMove(expected, setup, 4, 4)

    def testJailThirdRollBackToJail(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 3, monopoly.DontMove, monopoly.Jail)

    def testJailThirdRollDoublesBackToJail(self):
        setup = monopoly.Player(0, monopoly.Jail, 0, 2)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 6, 6, monopoly.Jail, monopoly.DontMove)

    def testGoBackThreeIncomeTax(self):
        setup = monopoly.Player()
        expected = monopoly.Player(1, 4)
        self._testMove(expected, setup, 4, 3, monopoly.GoBackThree, monopoly.DontMove)

    def testGoBackThreeNewYork(self):
        setup = monopoly.Player(0, 15)
        expected = monopoly.Player(1, 19)
        self._testMove(expected, setup, 4, 3, monopoly.GoBackThree, monopoly.DontMove)

    def testGoBackThreeDontMove(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, 33)
        self._testMove(expected, setup, 4, 3, monopoly.GoBackThree, monopoly.DontMove)

    def testGoBackThreeGo(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Go, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.GoBackThree, monopoly.Go)

    def testGoBackThreeJail(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Jail, 0, 0)
        self._testMove(expected, setup, 4, 3, monopoly.GoBackThree, monopoly.Jail)

    def testAdvanceWaterWorks(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.WaterWorks)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToUtility, monopoly.DontMove)

    def testAdvanceElectricCompany(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.ElectricCompany)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToUtility, monopoly.DontMove)

    def testAdvanceElectricCompanyGo(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.ElectricCompany, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToUtility, monopoly.DontMove)

    def testAdvanceReading(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Reading, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToRailroad, monopoly.DontMove)

    def testAdvancePennsylvania(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.PennsylvaniaRR)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToRailroad, monopoly.DontMove)

    def testAdvanceBandO(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.BandO)
        self._testMove(expected, setup, 4, 3, monopoly.AdvanceToRailroad, monopoly.DontMove)

    def testAdvanceBoardwalkGo(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.Boardwalk)
        self._testMove(expected, setup, 4, 3, monopoly.Boardwalk, monopoly.DontMove)

    def testAdvanceBoardwalkBandO(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.Boardwalk)
        self._testMove(expected, setup, 4, 3, monopoly.Boardwalk, monopoly.DontMove)

    def testAdvanceBoardwalkMarvinGardens(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Boardwalk)
        self._testMove(expected, setup, 4, 3, monopoly.Boardwalk, monopoly.DontMove)

    def testAdvanceIllinoisGo(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.Illinois)
        self._testMove(expected, setup, 4, 3, monopoly.Illinois, monopoly.DontMove)

    def testAdvanceIllinoisBandO(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.Illinois)
        self._testMove(expected, setup, 4, 3, monopoly.Illinois, monopoly.DontMove)

    def testAdvanceIllinoisMarvinGardens(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Illinois, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.Illinois, monopoly.DontMove)

    def testAdvanceReadingGo(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.Reading)
        self._testMove(expected, setup, 4, 3, monopoly.Reading, monopoly.DontMove)

    def testAdvanceReadingBandO(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.Reading, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.Reading, monopoly.DontMove)

    def testAdvanceReadingMarvinGardens(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.Reading, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.Reading, monopoly.DontMove)

    def testAdvanceStCharlesPlaceGo(self):
        setup = monopoly.Player(0, monopoly.Go)
        expected = monopoly.Player(1, monopoly.StCharlesPlace)
        self._testMove(expected, setup, 4, 3, monopoly.StCharlesPlace, monopoly.DontMove)

    def testAdvanceStCharlesPlaceBandO(self):
        setup = monopoly.Player(0, monopoly.PennsylvaniaRR)
        expected = monopoly.Player(1, monopoly.StCharlesPlace, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.StCharlesPlace, monopoly.DontMove)

    def testAdvanceStCharlesPlaceMarvinGardens(self):
        setup = monopoly.Player(0, monopoly.MarvinGardens)
        expected = monopoly.Player(1, monopoly.StCharlesPlace, 0, 3, 1)
        self._testMove(expected, setup, 4, 3, monopoly.StCharlesPlace, monopoly.DontMove)

if __name__ == '__main__':
    unittest.main()
